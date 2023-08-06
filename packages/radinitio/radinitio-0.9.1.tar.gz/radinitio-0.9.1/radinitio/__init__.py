import random, re, gzip, time, sys, argparse, os, multiprocessing, math
import numpy as np
from scipy.stats import poisson, binom
import msprime

#
# Copyright 2019, Julian Catchen <jcatchen@illinois.edu>
#
# This file is part of RADinitio.
#
# RADinitio is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RADinitio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RADinitio. If not, see <http://www.gnu.org/licenses/>.
#

#
# function to reverse complete sequence. It finds complement and inverts the order
def rev_comp(sequence):
    rev = []
    for nt in sequence.upper():
        if nt == 'A':
            rev.append('T')
        elif nt == 'C':
            rev.append('G')
        elif nt == 'G':
            rev.append('C')
        elif nt == 'T':
            rev.append('A')
        elif nt not in ['A', 'C', 'G', 'T']:
            rev.append('N')
    return ''.join(rev[::-1])

#
# function to load chromosome list into a set
# structure:      set('chrom1', 'chrom2', ... )
def chrom_set(chrom_listats_path):
    chrom_s = set()
    for line in open(chrom_listats_path, 'r'):
        chrom_s.add(line.strip('\n'))
    return chrom_s

#
# function to generate genome dictionary
# structure of this dictionary:     { chromosome_id : ATCGCAGGACTTACG... }
def load_genome(fasta_f, chrom_selection=None):
    assert chrom_selection is None or type(chrom_selection) == set
    # Create the empty dictionary
    genome_dict = dict()
    seq = []
    name = None
    # Allow reading of unzipped files
    fh = None
    if fasta_f[-3:] == '.gz':
        fh = gzip.open(fasta_f, 'rt')
    else:
        fh = open(fasta_f, 'r')
    # Open and process file handle
    for line in fh:
        line = line.strip('\n')
        if line[0] == '>':
            if name is not None:
                # Only add sequence if there is no chromosome
                # selection or if chromosome is in the selection.
                if name in chrom_selection or chrom_selection is None:
                    genome_dict[name] = ''.join(seq)
            # Have the sequence ID be only the chromosome ID and not the whole fasta header
            name = line[1:].split()[0]
            # Clear old sequence when new name is seen
            seq = []
        else:
            seq.append(line.upper())
    if name in chrom_selection or chrom_selection is None:
        genome_dict[name] = ''.join(seq)
    return genome_dict

# Function to generate the popmap from msprime model
def write_popmap(popmap_file, population_configurations, ploidity = 2):
    popmap = open(popmap_file, 'w')
    sample = 0
    sam_list = []
    # parse the population configurations and count samples
    for i, pop in enumerate(population_configurations):
        assert pop.sample_size % ploidity == 0
        for _ in range(pop.sample_size // ploidity):
            sam_list.append( (sample, i) )
            sample += 1
    # determine padding for samples and populations
    pad_s = '0{}d'.format(len(str(sam_list[-1][0])))
    pad_p = '0{}d'.format(len(str(sam_list[-1][1])))
    # Write popmap from sample list
    for s in sam_list:
        sam = 'msp_' + str(format(s[0], pad_s))
        pop = 'pop'  + str(format(s[1], pad_p))
        popmap.write('{}\t{}\n'.format(sam, pop))

#
# Functions for individual msprime simulation
def msprime_sim(length, recombination_rate, mutation_rate, population_configurations, migration_matrix=None):
    simulation = msprime.simulate(
        length=length,
        recombination_rate=recombination_rate,
        mutation_rate=mutation_rate,
        population_configurations=population_configurations,
        migration_matrix=migration_matrix)
    return simulation

#
# Function to do msprime simulations for all chromosomes
def sim_chromosomes(out_dir, chrom_lengths, chrom_recombination_rates, msprime_simulate_args, popmap_file, ploidity=2):
    out_dir = out_dir.rstrip('/')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    elif not os.path.isdir(out_dir):# or not os.path.readable(out_dir):
        sys.exit('oops')
    for chrom in sorted(chrom_lengths.keys()):
        # Run msprime simulation.
        simulation = msprime_sim(
            length = chrom_lengths[chrom],
            recombination_rate = chrom_recombination_rates[chrom],
            **msprime_simulate_args)
        # Write simulation output as VCF
        o_vcf_path = '{}/{}.vcf.gz'.format(out_dir, chrom)
        with gzip.open(o_vcf_path, 'wt') as vcf_file:
            simulation.write_vcf(vcf_file, ploidity)
        # TODO: Parallelize per chromosome
    # Generate popmap
    write_popmap(popmap_file, msprime_simulate_args['population_configurations'])

# Compatible enzymes
known_enzymes = { e[0].lower() : e for e in [
    ('EcoRI',   'G/AATTC'),
    ('SbfI',    'CC/TGCAGG'),
    ('PstI',    'C/TGCAG'),
    ('BamHI',   'G/GATCC'),
    ('HinDIII', 'A/AGCTT'),
    ('NotI',    'GC/GGCCGC'),
    ('MspI',    'C/CGG'),
    ('MseI',    'T/TAA')
    ]}

#
# set the restriction enzyme class and related variables
class RestrictionEnzyme:
    def __init__(self, enzyme_name):
        e = known_enzymes[enzyme_name.lower()]
        self.name = e[0]
        self.cutsite = e[1].replace('/', '')
        remainder_length = max([ len(part) for part in e[1].split('/') ])
        self.remainder = self.cutsite[len(self.cutsite)-remainder_length:]
    def olap_len(self):
        return 2 * len(self.remainder) - len(self.cutsite)

class LibraryOptions:
    def __init__(self,
                 library_type='baird',
                 renz_1='sbfI',
                 insert_mu=350,
                 insert_sigma=30,
                 min_distance=500,
                 coverage=20,
                 read_len=150,
                 ierr=0.001,
                 ferr=0.01):
        self.type = library_type                    # library type (ddRAD, sdRAD (aka baird))
        self.renz_1 = RestrictionEnzyme(renz_1)     # name of first restriction enzyme
        self.ins_mu = insert_mu                     # insert size mean
        self.ins_sig = insert_sigma                 # insert size standard deviation
        self.min_dist = min_distance                # mininum inter-locus distance
        self.cov = coverage                         # per-locus sequencing coverage
        self.rlen = read_len                        # read length in bp
        # TODO: add proper assert statements for the classes
        # TODO: generate log for the library parameters
        # TODO: add ddRAD parameters (ins_min = 250, ins_max = 500, renz_2)
        self.ins_len = lambda: int(np.random.normal(self.ins_mu, self.ins_sig))
        # Sequencing error parameters
        self.ierr = ierr                            # 5' error
        self.ferr = ferr                            # 3' error
        big_int = 1e6
        self.err_probs = (big_int,
            np.array([
                int( (self.ierr + (self.ferr - self.ierr) / (self.rlen - 1) * i) * big_int) for i in range(self.rlen)
                ], dtype=np.int64) )

#
# Reference Locus Class
class ReferenceLocus:
    def __init__(self, id, chromosome, cutsite_bp, start_bp, end_bp, sequence):
        self.id = id
        self.chrom = chromosome
        self.cut = cutsite_bp
        self.sta = start_bp
        self.end = end_bp
        self.seq = sequence
        self.dir = None
        if id[-1] == 'p':
            self.dir = 'positive'
        elif id[-1] == 'n':
            self.dir = 'negative'
#
# Function to find RAD loci in a chromosome sequence.
# Returns a list containing all the cutsite positions for a given sequence
def find_loci(chrom_name, chrom_sequence, library_options=LibraryOptions(), log_f=None):
    enz = library_options.renz_1
    raw_cuts = [ match.start() for match in re.finditer(enz.cutsite, chrom_sequence) ]
    # Filter cutsites
    kept_cutsites = []
    for i, cut in enumerate(raw_cuts):
        # Define locus boundary variables
        cutsite_first = cut
        cutsite_last  = cutsite_first + len(enz.cutsite) - 1
        forward_first = cutsite_first + (len(enz.cutsite) - len(enz.remainder))
        forward_last  = forward_first + 1000 - 1
        reverse_last  = cutsite_first + len(enz.remainder) - 1
        reverse_first = reverse_last - 1000 + 1
        min_distance  = library_options.min_dist
        status = None
        # Check if the cutsite is good.
        if reverse_last + 1 <= 1000 or forward_last + 1 >= len(chrom_sequence):
            # too close to chromosome end
            status = 'rm_chrom_end'
        elif i > 0 and cutsite_first - raw_cuts[i-1] < min_distance - enz.olap_len():
            # too close to another cutsite
            status = 'rm_too_close'
        elif i < len(raw_cuts) - 1 and raw_cuts[i+1] - cutsite_first < min_distance - enz.olap_len():
            # too close to another cutsite
            status = 'rm_too_close'
        else:
            status = 'kept'
            kept_cutsites.append(cut)
        # Write into log file
        if log_f is not None:
            log_f.write('{}\t{}\t{}\t{}\n'.format(
                chrom_name,
                cutsite_first,
                cutsite_last,
                status))
    return kept_cutsites

#
# Extract reference RAD loci from reference genome
# Returns dictionary of all loci ID and positions
# Also writes reference RAD loci fasta and statistics file
# TODO: parallelize
def extract_reference_rad_loci(genome_dict, out_dir, library_options=LibraryOptions()):
    # Check for class types and directories.
    assert type(genome_dict) == dict
    out_dir = out_dir.rstrip('/')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    elif not os.path.isdir(out_dir): # or not os.path.readable(out_dir):
        sys.exit('oops')
    # Open output FASTA and stats file.
    enz = library_options.renz_1
    fa_f = gzip.open('{}/reference_rad_loci_{}.fa.gz'.format(out_dir, enz.name), 'wt')
    stats_log = gzip.open('{}/reference_rad_loci_{}.stats.gz'.format(out_dir, enz.name), 'wt')
    stats_log.write('#chrom_id\tcut_pos_start\tcut_pos_end\tcutsite_status\n')
    # Loci ID information
    cuts_dict = dict()
    loc_num = 0
    # Loop throught chromosomes
    for chrom in sorted(genome_dict.keys()):
        # Find cutsites in that chromosome.
        cuts_dict[chrom] = find_loci(chrom, genome_dict[chrom], library_options=LibraryOptions(), log_f=stats_log)
    # Determine total number of kept cutsites
    total_cuts = sum([ len(cuts_dict[chrom]) for chrom in genome_dict.keys() ])
    # Create dictionary of all reference RAD loci
    # TODO: have this be a reference loci class
    loci_dict = dict()
    # Each locus is a ReferenceLocus() class object
    # loci_dict = { chrom1 : { loc1 : RefLoc1, loc2 : RefLoc2 },
    #               chrom2 : { loc3 : RefLoc3, loc4 : RefLoc4 } }
    # Loop throught chromosomes again and extract loci
    for chrom in sorted(genome_dict.keys()):
        chrom_loci = dict()   # Loci in this chromosome.
        # Loop through cutsites and process
        for i, cut in enumerate(cuts_dict[chrom]):
            # Define locus boundary variables
            cutsite_first = cut
            cutsite_last  = cutsite_first + len(enz.cutsite) - 1
            forward_first = cutsite_first + (len(enz.cutsite) - len(enz.remainder))
            forward_last  = forward_first + 1000 - 1
            reverse_last  = cutsite_first + len(enz.remainder) - 1
            reverse_first = reverse_last - 1000 + 1
            # Write information for the reverse locus...
            # ...into the loci dictionary
            l_id = 't{{:0{}d}}n'.format(len(str(total_cuts))).format(loc_num)
            seq = rev_comp(genome_dict[chrom][ reverse_first : reverse_last + 1 ])
            this_locus = ReferenceLocus(l_id, chrom, cutsite_first, reverse_first, reverse_last, seq)
            chrom_loci[l_id] = this_locus
            # ...into a fasta file
            fa_f.write('>{} ref_pos={}:{}-{}\n{}\n'.format(
                this_locus.id,
                this_locus.chrom,
                this_locus.sta + 1,
                this_locus.end + 1,
                this_locus.seq ))

            # Write information for the forward locus...
            # ...into the loci dictionary
            l_id = 't{{:0{}d}}p'.format(len(str(total_cuts))).format(loc_num)
            seq = genome_dict[chrom][ forward_first : forward_last + 1 ]
            this_locus = ReferenceLocus(l_id, chrom, cutsite_first, forward_first, forward_last, seq)
            chrom_loci[l_id] = this_locus
            # ...into a fasta file
            fa_f.write('>{} ref_pos={}:{}-{}\n{}\n'.format(
                this_locus.id,
                this_locus.chrom,
                this_locus.sta + 1,
                this_locus.end + 1,
                this_locus.seq ))
            loc_num += 1
        loci_dict[chrom] = chrom_loci
    return loci_dict

# Default substitution matrix. Equal probabilities for all substitutions.
#                            A    C    G    T
def_substitution_matrix = [[0.0, 1/3, 1/3, 1/3], # A
                           [1/3, 0.0, 1/3, 1/3], # C
                           [1/3, 1/3, 0.0, 1/3], # G
                           [1/3, 1/3, 1/3, 0.0]] # T

# Class defining substitution probabilities
class MutationModel:
    def __init__(
            self,
            substitution_matrix = def_substitution_matrix,
            indel_prob = 0.01,                         # 1% indels
            ins_del_ratio = 1.0,                       # 1:1 insertions and deletions
            indel_model = lambda: np.random.poisson(lam=1) ):
        sub_p = 1 - indel_prob                         # prob of a substitution
        del_p = indel_prob / (1 + ins_del_ratio)       # prob of a deletion
        ins_p = indel_prob - del_p                     # prob of an insertion
        m = substitution_matrix
        a, c, g, t = m[0], m[1], m[2], m[3]            # per nucleotide probs
        self.mutation_matrix = [
            (['C', 'G', 'T', 'I', 'D'],                # for ref = A
                [a[1]*sub_p, a[2]*sub_p, a[3]*sub_p, ins_p, del_p]),
            (['A', 'G', 'T', 'I', 'D'],                # for ref = C
                [c[0]*sub_p, c[2]*sub_p, c[3]*sub_p, ins_p, del_p]),
            (['A', 'C', 'T', 'I', 'D'],                # for ref = G
                [g[0]*sub_p, g[1]*sub_p, g[3]*sub_p, ins_p, del_p]),
            (['A', 'C', 'G', 'I', 'D'],                # for ref = T
                [t[0]*sub_p, t[1]*sub_p, t[2]*sub_p, ins_p, del_p]) ]
        self.indel_s = indel_model
    # Function to generate random mutations, like in PCR or sequencing error
    def random_mutation(self, ref):
        mutations_comb = {
            'A' : ['C','G','T'],
            'C' : ['A','G','T'],
            'G' : ['A','C','T'],
            'T' : ['A','C','G']}
        if ref == 'N':
            return 'N'
        else:
            return mutations_comb[ref][np.random.randint(3)]
    # Function to mutate reference allele for simulated variants
    def mutate(self, variant_position, chrom_sequence):
        nucleotides = ['A', 'C', 'G', 'T']
        ref = chrom_sequence[variant_position]
        alt = None
        if ref == nucleotides[0]:                     # for ref = A
            mut_pattern = self.mutation_matrix[0]
            alt = np.random.choice(mut_pattern[0], p = mut_pattern[1])
        elif ref == nucleotides[1]:                   # for ref = C
            mut_pattern = self.mutation_matrix[1]
            alt = np.random.choice(mut_pattern[0], p = mut_pattern[1])
        elif ref == nucleotides[2]:                   # for ref = G
            mut_pattern = self.mutation_matrix[2]
            alt = np.random.choice(mut_pattern[0], p = mut_pattern[1])
        elif ref == nucleotides[3]:                   # for ref = T
            mut_pattern = self.mutation_matrix[3]
            alt = np.random.choice(mut_pattern[0], p = mut_pattern[1])
        # else:
        #     assert False
        elif ref not in nucleotides:                  # for ref = N
            alt = 'N'
            return 'N','N'
        # Return values for substitutions
        if alt in nucleotides:
            assert ref != None or alt != None
            return ref, alt
        # Check for indels in alternative alleles
        elif alt in ['I', 'D']:
            # If Insertion
            if alt == 'I':
                size = 0
                # Determine size of insertion
                while size == 0:
                    size = self.indel_s()
                insert = [ref]
                for i in range(size):
                    insert.append(random.choice('ACGT'))
                # Return return ref and insertion
                assert ''.join(insert) != None or len(''.join(insert)) >= 1
                return ref, ''.join(insert)
            # If Deletion
            elif alt == 'D':
                deletion = None
                # Determine size of deletion
                size = 0
                while size == 0:
                    size = self.indel_s()
                # Determine position where deletion ends in sequence
                del_end = variant_position + size + 1
                # What if the mutation is on the last bp? Change to random substitution. This is unlikely, but its an important fix to have.
                if variant_position == len(chrom_sequence) - 1:
                    deletion = ref
                    ref = self.random_mutation(deletion)

                # For all other "normal" cases...
                if del_end <= len(chrom_sequence):
                    deletion = chrom_sequence[variant_position:del_end]
                else:
                    deletion = chrom_sequence[variant_position:len(chrom_sequence)]
                # Return deletion and ref
                return deletion, ref

#
# Function to merge msprime VCFs into master VCF
#
def merge_vcf(genome_dict,                       # Genome dictionary
              msp_vcf_dir,                       # Directory containing msprime VCFs
              out_dir,                           # Directory to save master VCF
              mutation_model=MutationModel() ):  # Mutation model class
    msp_vcf_dir = msp_vcf_dir.rstrip('/')
    out_dir = out_dir.rstrip('/')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    elif not os.path.isdir(out_dir):# or not os.path.readable(out_dir):
        sys.exit('oops')
    # open output file
    out_f = gzip.open('{}/ri_master.vcf.gz'.format(out_dir), 'wt')
    # work on the vcf header
    out_f.write('##fileformat=VCFv4.2\n##source=RADinitio - merge_vcf()\n##FILTER=<ID=PASS,Description="All filters passed">\n')
    for chrom in sorted(genome_dict.keys()):
        out_f.write('##contig=<ID={},length={}>\n'.format(chrom,len(genome_dict[chrom])))
    out_f.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
    # Loop throught chromosomes
    for chr_i, chrom in enumerate(sorted(genome_dict.keys())):
        # Extract working sequence
        seq = genome_dict[chrom]
        prev_pos = 0
        # Open msprime VCF
        for line in gzip.open('{}/{}.vcf.gz'.format(msp_vcf_dir, chrom), 'rt'):
            # Extract vcf header
            msp = []
            iden = []
            # Process sample IDs
            if line[0] == '#':
                if line[0:6] == '#CHROM' and chr_i == 0:
                    fields = line.strip('\n').split('\t')
                    for f in fields:
                        if f[0:3] == 'msp':
                            msp.append(f)
                        else:
                            iden.append(f)
                    # Determine pad size based on the length of largest sample number
                    pad = '0{}d'.format(len(msp[-1][4:]))
                    for m in range(len(msp)):
                        iden.append('msp_' + str(format(m, pad)))
                    out_f.write('\t'.join(iden)+'\n')
                continue
            # Process alleles
            fields = line.strip('\n').split('\t')
            pos = int(fields[1]) - 1 # 0-based position of the SNP in the reference sequence
            # In case any simulated positions are larger than the reference chromosome...
            if pos >= len(seq):
                break
            fields[0] = chrom # chromosome ID
            # Remove variants if they are overlapping with indel sizes
            if pos <= prev_pos:
                continue
            # determine the new sequences of the reference and alternative alleles
            fields[3], fields[4] = mutation_model.mutate(pos, seq)
            # If we are dealing with an indel, increase the prev_pos value.
            if len(fields[3]) > 1 or len(fields[4]) > 1:
                prev_pos = pos + len(fields[3])
            # Remove Ns
            if fields[3] == 'N':
                continue
            # Write new VCF line
            out_f.write('\t'.join(fields)+'\n')

#
# Function to create a RAD position set dictionary for variant filtering
# Input is the 'loci_dict' from 'extract_reference_rad_loci()'
def create_rad_pos_set_dict(loci_dict):
    # Create empty output dictionary
    pos_set_dict = dict()
    # iterate over chroms in loci_dict
    for chrom in sorted(loci_dict.keys()):
        curr_chrom_dict = dict()
        # Iterate over the chromosome's loci
        for locus in sorted(loci_dict[chrom].keys()):
            curr_locus = loci_dict[chrom][locus]
            # Select data current locus
            l_sta = curr_locus.sta
            l_end = curr_locus.end + 1
            # iterate over range in locus
            for bp in range(l_sta, l_end):
                curr_chrom_dict.setdefault(bp, []).append(locus)
        pos_set_dict[chrom] = curr_chrom_dict
    return pos_set_dict

#
# Set the Variant class and related variables
# Structure: (locus_id, bp, A, T, 1101100010)
class Variant:
    def __init__(self, locus_id, position_bp, ref_allele, alt_allele, genotypes):
        self.loc = locus_id
        self.pos  = position_bp
        self.ref  = ref_allele
        self.alt  = alt_allele
        self.geno = genotypes
        # Set the different types of variants
        self.type = None
        if len(self.ref) == len(self.alt):
            self.type = 'substitution'
        elif len(self.ref) > 1:
            self.type = 'deletion'
        elif len(self.alt) > 1:
            self.type = 'insertion'
    # Function to extract specific genotype from 'geno' string
    def get_genotype(self, sample_i, allele_n):
        assert allele_n in [0, 1]
        genotype = int(self.geno[ (sample_i * 2) + allele_n ])
        assert genotype in [0, 1]
        return genotype
#
# Function to find and filter the RAD variants based on cutsite information
def filter_rad_variants(loci_dict, pos_set_dict, m_vcf_dir, library_opts=LibraryOptions()):
    m_vcf_pdir = m_vcf_dir.rstrip('/')
    # create empty rad variant_dictonary
    # rad_variants_dict = { loc1 : [var1, var2, ...] , loc2 : [var1], loc3 : [] }
    rad_variants_dict = dict()
    # Open master VCF
    for line in gzip.open('{}/ri_master.vcf.gz'.format(m_vcf_dir), 'rt'):
        if line[0] == '#':
            # Skip comment and metadata lines
            continue
        else:
            fields = line.strip('\n').split('\t')
            chrom = fields[0]
            pos = int(fields[1]) - 1
            # Verify is variant is in RAD loci
            which_locus = pos_set_dict.get(chrom, dict()).get(pos)
            if which_locus == None:
                # Means pos is NOT in rad loci
                continue
            elif len(which_locus) > 1:
                # This means the position is shared across multiple loci
                # TODO: decice what to do for shared variants. Most of these will be on the cutsite
                continue
            else:
                # Process the variants
                curr_locus = loci_dict[chrom][which_locus[0]]
                column = 0.0
                ref_a = fields[3]
                alt_a = fields[4]
                genotypes = []
                for i in range(9, len(fields)):
                    genotypes.append(fields[i][0])
                    genotypes.append(fields[i][2])
                genotypes = ''.join(genotypes)
                # Process negative loci
                if curr_locus.dir == 'negative':
                    # TODO: check that indels are rev_comp correctly (I see some weird behavior)
                    ref_a = rev_comp(ref_a)[::-1] # these are necessary for indels (double check)
                    alt_a = rev_comp(alt_a)[::-1]
                    # convert bp to reverse col 5'->3'
                    column = curr_locus.end - pos # TODO: extra testing on this
                # Process positive loci
                elif curr_locus.dir == 'positive':
                    # readjust from bp to col
                    column = pos - curr_locus.sta
                # (loci_id, pos1, A, T, gt1gt2gt3gt4)
                variant = Variant(curr_locus.id, column, ref_a, alt_a, genotypes)
                # add to variant dictionary
                rad_variants_dict.setdefault(curr_locus.id, []).append(variant)
            # TODO: produce RAD VCF including dropped alleles
            # TODO: parallelize per chromosome?
    return rad_variants_dict

#
# Function to extract alleles
def extract_rad_alleles(loci_dict, rad_variants_dict, popmap_file, out_dir, library_opts=LibraryOptions(), ploidity = 2):
    # Check output directory
    out_dir = out_dir.rstrip('/')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    elif not os.path.isdir(out_dir): # or not os.path.readable(out_dir):
        sys.exit('oops')
    # generate a sample list from popmap
    samples = []
    for sample in open(popmap_file, 'r'):
        samples.append(sample.strip('\n').split('\t')[0])
    # set restriction enzyme
    enz = library_opts.renz_1
    # Iterate over the samples
    # TODO: split this into smaller function for parallelization
    for s_i, sample in enumerate(samples):
        # create an output file for the sample
        al_fasta = gzip.open('{}/{}.{}_alleles.fa.gz'.format(out_dir, sample, enz.name), 'wt')
        # iterate over the loci dictionary
        for chrom in sorted(loci_dict.keys()):
            for loc_id in sorted(loci_dict[chrom].keys()):
                # Set sequence and variant info for the current locus
                curr_locus = loci_dict[chrom][loc_id]
                curr_vars = rad_variants_dict.get(curr_locus.id, []) # In case there are loci with no variants
                # Iterate over the number of alleles
                for allele in range(ploidity):
                    # Check if cutsite needs to be discarded
                    discard = False
                    # Create copy of the locus
                    seq_copy = list(curr_locus.seq)
                    # Iterate over the variants
                    for var in curr_vars:
                        # TODO: set the CIGARs
                        # print(var.loc, var.pos, var.ref, var.alt, var.type, var.geno)
                        # Check genotype
                        if var.get_genotype(s_i, allele) == 1:
                            # For substitutions
                            if var.type == 'substitution':
                                seq_copy[var.pos] = var.alt
                            # For insertions
                            elif var.type == 'insertion':
                                seq_copy[var.pos] = var.alt
                            # For deletions
                            elif var.type == 'deletion':
                                for bp in range(len(var.ref) - 1):
                                    # in deletions, you delete the nucleotides AFTER the variant position
                                    d_i = var.pos + bp + 1
                                    seq_copy[d_i] = ''
                    allele_seq = ''.join(seq_copy)
                    # Check cutsite
                    if allele_seq[:len(enz.remainder)] != enz.remainder:
                        discard = True
                    # Remove if needed
                    if discard == True:
                        continue
                    # Save sequences into output file
                    # TODO: print cigar
                    cig = '1000M'
                    al_fasta.write('>{}:{}:a{:d} cig={}\n{}\n'.format(curr_locus.id, sample,  allele+1, cig, allele_seq))

#
# Function to load the alleles of a single sample
def load_sample_alleles(sample_name, alleles_dir, library_opts=LibraryOptions()):
    # Check input directory
    alleles_dir = alleles_dir.rstrip('/')
    if not os.path.isdir(alleles_dir): # or not os.path.readable(out_dir):
        sys.exit('oops')
    # Set library parameters
    enz = library_opts.renz_1
    # Create allele list
    alleles_list = []
    header = None
    # Open file and read
    alleles_fa = '{}/{}.{}_alleles.fa.gz'.format(alleles_dir, sample_name, enz.name)
    for line in gzip.open(alleles_fa, 'rt'):
        if line[0] == '>':
            header = line[1:-1]
        else:
            alleles_list.append( (header, line[:-1]) )
    return alleles_list

#
# Determine number of avergge reads from
# the number of loci and coverage
# TODO: Make compatible with ddRAD
def avg_num_reads(genome_dict, library_opts=LibraryOptions()):
    # raw number of cuts
    cut_n = 0
    # Iterate over genome dict
    for chrom in sorted(genome_dict.keys()):
        chr_loci = find_loci(chrom, genome_dict[chrom], library_opts)
        cut_n += len(chr_loci)
    assert cut_n != None
    # Calculate number of loci, two per cutsite
    loci_n = cut_n * 2
    # Calculate number of reads, loci x coverage
    assert library_opts.cov != None
    n_reads = loci_n * library_opts.cov
    return n_reads

#
# Determine number of desired reads to obtain a coverage
def target_reads(n_alleles, coverage):
    n_reads = (n_alleles // 2) * coverage
    return int(n_reads)

# sample and process a template molecule from all available alleles
def sample_a_template(alleles_list, library_opts=LibraryOptions()):
    allele = random.choice(alleles_list)
    insert_len = 0
    while not library_opts.rlen <= insert_len <= len(allele[1]):
        insert_len = library_opts.ins_len()
    return allele, insert_len

# Split CIGAR string into CIGAR list
def split_cigar_str(cigar):
    splitcig = []
    prev = 0
    for i, c in enumerate(cigar):
        if c in ('M', 'I', 'D'):
            splitcig.append(cigar[prev:i+1])
            prev=i+1
    return splitcig

#
# Extracts a read CIGAR from its locus CIGAR.
def extract_read_cigar(cigar, start, read_len, allele_seq):
    # Convert CIGAR from CIGAR string to CIGAR list
    cig_l = split_cigar_str(cigar)
    cig_n = []
    ref_consumed = 0
    ref_len = len(allele_seq)
    read_consumed = 0
    # Check CIGAR operations
    for op in cig_l:
        type = op[-1]
        if not type in ('M','D','I'):
            raise Exception('MDI')
        size = int(op[:-1])
        # Fast forward to the read region.
        if len(cig_n) == 0:
            # For Matches
            if type == 'M':
                if ref_consumed + size <= start:
                    ref_consumed += size
                    continue
                elif ref_consumed < start:
                    consume = start - ref_consumed
                    ref_consumed += consume
                    size -= consume
            # For Deletions
            if type == 'D':
                start += size
                ref_consumed += size
                continue
            # For Insertions
            elif type == 'I':
                start -= size
                if ref_consumed <= start:
                    continue
                else:
                    size = ref_consumed - start
            # For Clipped regions at the end
            if ref_consumed > 0:
                cig_n.append('{}H'.format(ref_consumed))
        # Write the cigar operations within the reads.
        if type == 'M': # For Match
            consume = min(size, read_len - read_consumed)
            cig_n.append('{}M'.format(consume))
            read_consumed += consume
            ref_consumed += consume
        elif type == 'D': # For Dels
            cig_n.append(op)
            ref_consumed += size
        elif type == 'I': # For Ins
            consume = min(size, read_len - read_consumed)
            cig_n.append('{}I'.format(consume))
            read_consumed += consume
        # Break after the read.
        if read_consumed == read_len:
            if ref_consumed < ref_len:
                cig_n.append('{}H'.format(ref_len - ref_consumed))
            break
        else:
            assert read_consumed < read_len
    # Return new CIGAR string for the read
    return cig_n

# generate new name for a sampled template
def build_base_template_name(allele, insert_len, clone_i, library_opts=LibraryOptions()):
    # produce read name
    fields = allele[0].split(' ')
    # TODO: Process CIGAR
    assert fields[1].startswith('cig=')
    cigar = fields[1][len('cig='):]
    fw_read_cig = ''.join( extract_read_cigar(cigar, 0, library_opts.rlen, allele[1]) )
    rev_read_cig = ''.join( extract_read_cigar(cigar, (insert_len - library_opts.rlen), library_opts.rlen, allele[1])[::-1] )
    name = '{}:cig1={}:cig2={}:{}'.format(fields[0], fw_read_cig, rev_read_cig, clone_i + 1)
    return name

#
# Generate new sequence with a PCR mutation
def introduce_pcr_mutation(seq, insert_len, library_opts=LibraryOptions(), mutation_model=MutationModel()):
    # Define forward and reverse read intervals within the sequence
    read_regions = list(range(0, library_opts.rlen)) + list(range((insert_len - library_opts.rlen), insert_len))
    # Choose a random position in sequence within the read regions
    pos = random.choice(read_regions)
    # Find alternative nucleotide for that position
    nuc = mutation_model.random_mutation(seq[pos])
    return seq[:pos] + nuc + seq[pos+1:]

#
# Function to add sequencing errors to a sequence.
# `err_probs` as defined by LibraryOptions classs
def seq_error(seq, err_probs, mutation_model=MutationModel()):
    # Make sure size of errors is the same as the read length
    assert len(err_probs[1]) == len(seq)
    lseq = list(seq)
    # Generate random integer list and compare agains err_probs
    rdm = np.random.randint(err_probs[0], size=len(seq))
    for i in range(len(seq)):
        if rdm[i] < err_probs[1][i]:
            lseq[i] = mutation_model.random_mutation(lseq[i])
    return ''.join(lseq)

# function to generate template molecule (sheared allele sequence)
# Simulate sequencing process for a given read pair
def sequence_read_pair(allele, insert_len, library_opts=LibraryOptions()):
    fw_read = seq_error(allele[1][:library_opts.rlen], library_opts.err_probs)
    rv_read = rev_comp(seq_error(allele[1][(insert_len - library_opts.rlen):insert_len], library_opts.err_probs))
    return fw_read, rv_read

#
# PCR Model
#

# Determine number of per-clone PCR duplicates (size of clone)
def simulate_pcr_inherited_efficiency(mu, sigma, n_cycles):
    duplicates = 1
    #p = 0.5       # Probability of duplicating a read
    p = 0.0
    while not 0.0 < p <= 1.0:
        p = np.random.normal(mu, sigma)
    for i in range(n_cycles):
        duplicates += np.random.binomial(duplicates, p)
    return duplicates

# Overall distribution of PCR duplicates
#  This will determine clone size and frequency (probability)
#  Structure: Cpn, where p is the frequency of a clone of size n
#     [ Cp0, Cp1, Cp2, Cp3, Cp4, ... ]
def get_library_clone_size_distribution(pcr_model, n_sims=1e5):
    clone_histogram = {}
    for i in range(int(n_sims)):
        clone_size = pcr_model()
        clone_histogram.setdefault(clone_size, 0)
        clone_histogram[clone_size] += 1
    max_size = max(clone_histogram.keys())
    for i in range(max_size+1):
        clone_histogram.setdefault(i, 0)
    clone_histogram = [ clone_histogram[i] / n_sims for i in range(max_size+1) ]
    return clone_histogram

#
# Function to log convert the size clases of the amplified clone size distribution
# Converting the distribution will collapse size classes, decreasing the size of the distribution and improving efficiency
def log_convert_ampl_clone_dist(ampl_clone_size_distrib, base):
    # generate empy distribution of size x, where x is the log of the biggest clone in the original distribution
    a_max = len(ampl_clone_size_distrib) - 1
    log_ampl_clone_size_distrib = [ 0.0 for log_a in range(math.floor(math.log(a_max, base)) + 1) ]
    for a, prob in enumerate(ampl_clone_size_distrib):
        if a == 0:
            continue
        log_a = math.floor(math.log(a, base))
        log_ampl_clone_size_distrib[log_a] += prob
    assert 1.0-1e-9 < sum(log_ampl_clone_size_distrib) < 1.0+1e-9
    return log_ampl_clone_size_distrib

#
# Function to determine the clone sizes within a clone class
# log_a = is the log-transform of a clone size
def get_sizes_in_clone_class(log_a, base):
    assert log_a >= 0
    clone_class = range(
        math.ceil(base ** log_a),
        math.ceil(base ** (log_a + 1)) )
    if not clone_class:
        return None
    return clone_class
def get_clone_class_representative_value(log_a, base):
    if get_sizes_in_clone_class(log_a, base) is None:
        return None
    return round(base ** (log_a + 0.5))

#
# Calculate number of starting templates
def total_molecules_per_sample(insert_bp, dna_ng, n_samples, frac_rad_molecules=0.01):
    # The fraction of "good" RAD molecules when amplifying library.
    # Takes into account frequency of cuts, size selection, adapters, etc.
    avog = 6.022e23
    nuc_w = 660
    total_molecules = (( dna_ng * avog ) / ( insert_bp * 1e9 * nuc_w)) * frac_rad_molecules
    return int(total_molecules//n_samples)

#
# Calculate total number of template molecules based on the template/read ratio
def total_template_molecules(n_sequenced_reads, ratio):
    assert n_sequenced_reads != None
    assert n_sequenced_reads > 0
    assert ratio != None
    template_n = n_sequenced_reads * ratio
    return template_n
#
# Total number of amplified molecules obtaining during the PCR amplification process
def get_total_amplified_molecules(ampl_clone_size_distrib, n_templates, base):
    assert n_templates != None
    assert n_templates > 0
    total_amplified_molecules = 0.0
    for log_a, prob in enumerate(ampl_clone_size_distrib):
        a = get_clone_class_representative_value(log_a, base)
        if a is None:
            assert prob == 0.0
            continue
        total_amplified_molecules += a * prob
    total_amplified_molecules *= n_templates
    return int(total_amplified_molecules)

#
# Calculate number of mutated nodes in PCR clone tree
def mutated_node_freq(n_nodes):
    # 0 and 1 can never have mutations
    assert n_nodes >= 2
    # edges are the number of sucessful amplification reactions
    n_edges = n_nodes - 1
    # Mutations appear on a random edge
    edge_with_mut = np.random.randint(n_edges)
    # List storing the nodes count
    #   [no_mutations, mutations]
    nodes_cnt = [1 + edge_with_mut, 1]
    # Determine if later reactions stem from mutated node
    while (nodes_cnt[1] + nodes_cnt[0]) < n_nodes:
        # Prob of new mutated node
        p = nodes_cnt[1] / (nodes_cnt[1] + nodes_cnt[0])
        # Prob of new non-mutated node
        q = 1 - p
        # Select if new node is mutated (1) or not (0)
        i = np.random.choice([1, 0], p=[p, q])
        nodes_cnt[i] += 1
    # Return number of mutated nodes in the tree
    return nodes_cnt[1]

#
# Calculate the probability of obtaining no mutations in a given clone size
def prob_pcr_no_error(ampl_clone_size, read_len, pol_error):
    if ampl_clone_size <= 1:
        return 1.0
    else:
        p_no_err_read = (1 - pol_error) ** ((ampl_clone_size - 1) * (read_len * 2))
        return p_no_err_read

#
# Generate distribution of per clone probabilities of no error
#   Structure:  [ error_prob0, error_prob1, ... ]
def per_clone_no_error_prob_log_dist(read_len, log_ampl_clone_size_distrib, base, pol_error=4.4e-7):
    # pol_error default is the fidelity of Phusion HF Pol (per bp, per CPR cycle)
    per_clone_no_error = [ None for log_a in range(len(log_ampl_clone_size_distrib)) ]
    for log_a in range(len(log_ampl_clone_size_distrib)):
        a = get_clone_class_representative_value(log_a, base)
        if a is None:
            continue
        per_clone_no_error[log_a] = prob_pcr_no_error(a, read_len, pol_error)
    # Return list of error probabilities for the corresponding clone sizes classes
    return per_clone_no_error

#
# Per clone size, generate a distribution of the frequency of nodes with mutation
#   Structure: [ [ p0, p1, p2 ]
#                [ p0, p1, p2, p3 ],
#                ...,
#                [ p0, p1, p2, ..., pn ] ]
# First dimension of the list is the clone size classes, starting at class size 2 (0 & 1 have no error)
# Second dimension is distribution of errors in that clone
def generate_mut_node_log_distrib(log_ampl_clone_size_distrib, base, max_iter):
    # Empty list to hold the error distributions for all clone size classes
    mut_node_dist = [ None for log_a in range(len(log_ampl_clone_size_distrib)) ]
    # Iterate over the size classes
    for log_a in range(len(log_ampl_clone_size_distrib)):
        a = get_clone_class_representative_value(log_a, base)
        if a is None:
            continue
        if a < 2:
            continue
        # Iterate and keep tally of the mutated nodes generated
        clone_error_dist = [ 0 for n_mut in range(a + 1) ]
        for _ in range(max_iter):
            n_mut = mutated_node_freq(a)
            clone_error_dist[n_mut] += 1
        # Convert tally to frequency list
        mut_freq = [ clone_error_dist[n_mut]/max_iter for n_mut in range(a + 1) ]
        # Store in mut_node_dist list
        mut_node_dist[log_a] = mut_freq
    return mut_node_dist

#
# New distribution containing the adjusted mutated molecule distribution
# Merges `per_clone_no_error_prob_dist` and `generate_mut_node_distrib`
#   Structure: [ [ p0 ],
#                [ p0, p1 ], ...,
#                [ p0, p1, p2, ..., pn ] ]
# First dimension of the list is the clone size classes,
# Second dimension is distribution of errors in that clone
def adjust_dist_of_ampl_errors(log_ampl_clone_size_distrib, read_len, 
        base, max_iter=100, pol_error=4.4e-7):
    # Generate two base distributions
    clone_no_error_prob = per_clone_no_error_prob_log_dist(read_len, log_ampl_clone_size_distrib, base)
    mut_node_dist = generate_mut_node_log_distrib(log_ampl_clone_size_distrib, base, max_iter=100)
    assert len(clone_no_error_prob) == len(mut_node_dist)
    adj_error_dist = [ None for log_a in range(len(clone_no_error_prob)) ]
    for log_a, prob_no_mut in enumerate(clone_no_error_prob):
        if prob_no_mut is None:
            continue
        if log_a == 0:
            # a==1; no mutations.
            adj_error_dist[0] = [1.0, 0.0]
            continue
        assert mut_node_dist[log_a][0] == 0.0
        assert 1.0-1e-9 < sum(mut_node_dist[log_a]) < 1.0+1e-9
        adj_error_dist[log_a] = [ p_n_mut * (1 - prob_no_mut) for p_n_mut in mut_node_dist[log_a] ]
        adj_error_dist[log_a][0] = prob_no_mut
    return adj_error_dist

#
# Generate a single distribution containing both PCR error and duplicates by
# applying the following formula:
# p(S=s^ES=r) = sum_a{ p(A=a) p(S=s|A=a) sum_e{ p(EA=e|A=a) p(ES=r|S=s^A=a^EA=e) }}
def generate_pcr_dups_error_log_distrib(log_ampl_clone_size_distrib, n_sequenced_reads,
        total_amplified_molecules, base, single_adj_error_distrib=None):
    max_s = 1000    # Max size of sequenced clones
    p_lim = 1e-6    # Truncate distribution for values smaller than this
    seq_pcr_error_distrib = []
    #   Structure: [ [ p0 ],
    #                [ p0, p1 ], ...,
    #                [ p0, p1, p2, ..., pn ] ]
    # Half matrix containing probabilities of clone sizes and error
    # First dimension clone sizes
    # Second dimension errors in that clone size

    # Define the amplifed clone size classes
    a_classes = range(len(log_ampl_clone_size_distrib))
    # precompute the p(S=s|A=a)
    p_s_a = [None for log_a in a_classes]
    for log_a in a_classes:
        a = get_clone_class_representative_value(log_a, base)
        if a is None:
            continue
        p_s_a[log_a] = poisson.pmf(range(max_s), (n_sequenced_reads * a / total_amplified_molecules))
    p_s0 = None
    for s in range(max_s):
        seq_pcr_error_distrib.append([ None for r in range(s+1) ])
        # precompute the p(ES=r|S=s^A=a^EA=e)
        if single_adj_error_distrib is not None:
            p_r_sae = []
            for log_a in a_classes:
                p_r_sae.append(None)
                a = get_clone_class_representative_value(log_a, base)
                if a is None:
                    continue
                p_r_sae[-1] = [ binom.pmf(range(s+1), s, e/a) for e in range(a+1) ]
        for r in range(s+1):
            p_sr = 0.0
            for log_a in a_classes:
                a = get_clone_class_representative_value(log_a, base)
                if a is None:
                    continue
                if single_adj_error_distrib is None:
                    sum_e = 1.0 if r == 0 else 0.0
                else:
                    sum_e = 0.0
                    for e in range(a):
                        # sum_e{ p(EA=e|A=a) p(ES=r|S=s^A=a^EA=e)
                        p_e_a = single_adj_error_distrib[log_a][e]
                        sum_e += p_e_a * p_r_sae[log_a][e][r]
                # sum_a{ p(A=a) p(S=s|A=a) sum_e{ p(EA=e|A=a) p(ES=r|S=s^A=a^EA=e) }} for a given `a`
                p_sr += log_ampl_clone_size_distrib[log_a] * p_s_a[log_a][s] * sum_e
            if s == 0 :
                assert r == 0
                p_s0 = p_sr
                seq_pcr_error_distrib[0][0] = 0.0
            else:
                seq_pcr_error_distrib[s][r] = p_sr / (1 - p_s0)
        if s > 0 and sum(seq_pcr_error_distrib[s]) < p_lim:
            # break when values are getting too small
            break
    assert len(seq_pcr_error_distrib) > 1
    # Return double matrix
    return seq_pcr_error_distrib

#
# Convert the sequenced clone/error matrix into two lists (one of values and one of probabilities)
# Values are (x, y), where x is a sequenced clone size, y is number of molecules with error in that sequenced clone
def get_seq_pcr_error_lists(seq_pcr_error_distrib):
    seq_clone_errors_freq = []
    seq_clone_errors_vals = []
    for s, probs in enumerate(seq_pcr_error_distrib):
        for r, p in enumerate(probs):
            seq_clone_errors_freq.append(p)
            seq_clone_errors_vals.append((s, r))
    # Adjust values so sum of probabilities equals 1
    #   This is product of truncating the distribution for really small values
    sum_p = np.sum(seq_clone_errors_freq)
    if sum_p < 1:
        seq_clone_errors_freq = [ seq_clone_errors_freq[i]/sum_p for i in range(len(seq_clone_errors_freq)) ]
    # Return lists of clone values and adjusted frecuency
    return seq_clone_errors_freq, seq_clone_errors_vals

#
# Convert distribution of clone sizes AND errors into clone sizes only
def get_duplicate_only_distrib(seq_clone_errors_freq, seq_clone_errors_vals):
    dup_distrib = {}
    # Iterate over the clone+error distribution and sum all frequencies for a given clone size
    for i in range(len(seq_clone_errors_freq)):
        clone_size = seq_clone_errors_vals[i][0]
        dup_distrib.setdefault(clone_size, 0)
        dup_distrib[clone_size] += seq_clone_errors_freq[i]
    dup_distrib = [ dup_distrib[clone_size] for clone_size in sorted(dup_distrib.keys()) ]
    # Return a list containing the per-sequenced clone size frequencies
    return dup_distrib

#
# From the distribution of sequenced clones, calculate the percentage of PCR duplicates
def calculate_perc_duplicates(dup_distrib):
    # duplicates = to 1 - (1 / sum_reads)
    # sum_reads = 1*p(S=1) + 2*p(S=2) + 3*p(S=3) + ...
    # 1 - sum_reads is the portion of reads that are kept
    sum_reads = 0.0
    for clone_size, prob in enumerate(dup_distrib):
        if clone_size == 0:
            continue
        # Do n*p(S=n), where n is the clone size
        sum_reads += (clone_size * prob)
    # Return 1 - kept_reads
    return 1 - (1 / sum_reads)

#
# Sample from the merged sequencing clone size/error distribution and
# determine the properties of the sequenced clone
def determine_seq_clone_size_error(seq_clone_errors_freq, seq_clone_errors_vals):
    value_index = list(range(len(seq_clone_errors_vals)))
    seq_clone_index = np.random.choice(value_index, p=seq_clone_errors_freq)
    # First value is size of the clone
    clone_size = seq_clone_errors_vals[seq_clone_index][0]
    # Second value is number of mutated molecules in clone
    clone_error = seq_clone_errors_vals[seq_clone_index][1]
    return clone_size, clone_error

#
# PCR duplicates class
class PCRDups:
    def __init__(self,
                 pcr_c=0,
                 n_sequenced_reads=None,
                 pcr_mod_mu=0.45,
                 pcr_mod_sd=0.2,
                 temp_ratio=2.0, # TODO: good default value?
                 base=(2**0.1),
                 max_iter=100,
                 pol_error=4.4e-7,
                 library_opts=LibraryOptions()):
        self.pcr_cyc = pcr_c
        if self.pcr_cyc > 0 and n_sequenced_reads == None:
            sys.exit('\tIf performing PCR, a number of target reads is necessary.\n\tCheck `avg_num_reads()` function.')
        self.pcr_mu  = pcr_mod_mu
        self.pcr_sig = pcr_mod_sd
        self.ratio   = temp_ratio
        self.base    = base
        self.max_it  = max_iter
        self.pol_er  = pol_error
        self.n_reads = n_sequenced_reads
        # self.n_temps = None
        # If no PCR cycles, return empty PCR clone distribution, otherwise generate distribution
        self.seq_clone_errors_freq = None
        self.seq_clone_errors_vals = None
        if self.pcr_cyc == 0:
            # If PCR cycles is None, only the (1, 0) clone is possible
            self.seq_clone_errors_vals = [(0, 0), (1, 0)]
            self.seq_clone_errors_freq = [0.0, 1.0]
        else:
            # Amplified PCR duplicate distribution:
            pcr_model = lambda: simulate_pcr_inherited_efficiency(self.pcr_mu, self.pcr_sig, self.pcr_cyc)
            ampl_clone_size_distrib = get_library_clone_size_distribution(pcr_model)
            # Log convert amplified clone size distribution
            log_ampl_clone_size_distrib = log_convert_ampl_clone_dist(ampl_clone_size_distrib, self.base)
            # Adjusted amplified PCR error distribution
            single_adj_error_distrib = adjust_dist_of_ampl_errors(log_ampl_clone_size_distrib, library_opts.rlen, self.base, self.max_it, self.pol_er)
            # Calculate number of template molecules in the PCR reaction
            self.n_temps = total_template_molecules(self.n_reads, self.ratio)
            # Amplified pool size in PCR reaction
            total_amplified_molecules = get_total_amplified_molecules(log_ampl_clone_size_distrib, self.n_temps, self.base)
            # Generate a single distribution that convined probabilities of duplicates and error for PCR clones
            seq_pcr_error_distrib = generate_pcr_dups_error_log_distrib(
                log_ampl_clone_size_distrib,
                self.n_reads,
                total_amplified_molecules,
                self.base,
                single_adj_error_distrib)
            # Convert the matrix into two lists (one of values and one of probabilities)
            self.seq_clone_errors_freq, self.seq_clone_errors_vals = get_seq_pcr_error_lists(seq_pcr_error_distrib)
        # Convert into single list of clone sizes and calculate PCR duplicates
        dup_distrib = get_duplicate_only_distrib(self.seq_clone_errors_freq, self.seq_clone_errors_vals)
        self.perc_duplicates = calculate_perc_duplicates(dup_distrib)
        # TODO: generate logs for the PCR distributions
    # Sample from the merged sequencing clone size/error distribution and
    # determine the properties of the sequenced clone
    def determine_seq_clone_size_error(self):
        value_index = list(range(len(self.seq_clone_errors_vals)))
        seq_clone_index = np.random.choice(value_index, p=self.seq_clone_errors_freq)
        # First value is size of the clone
        clone_size = self.seq_clone_errors_vals[seq_clone_index][0]
        # Second value is number of mutated molecules in clone
        clone_error = self.seq_clone_errors_vals[seq_clone_index][1]
        return clone_size, clone_error

#
# Extract reads from a sample
def sequence_sample(sample_n, out_dir, alleles_list, library_opts=LibraryOptions(), mutation_opts=MutationModel(), pcr_opts=PCRDups()):
    # Open output files
    reads1_fa = gzip.open('{}/{}.1.fa.gz'.format(out_dir, sample_n), 'wt')
    reads2_fa = gzip.open('{}/{}.2.fa.gz'.format(out_dir, sample_n), 'wt')
    # Determine the number of reads to generate
    n_sequenced_reads = target_reads(len(alleles_list), library_opts.cov)
    # Loop over target reads and sequence each iteration
    remaining_reads = n_sequenced_reads
    clone_i = 0
    while remaining_reads > 0:
        # Sample random template to start a clone
        allele, insert_len = sample_a_template(alleles_list, library_opts)
        base_name = build_base_template_name(allele, insert_len, clone_i, library_opts)
        # Determine size of clone and number of reads with mutations
        clone_size, n_mut_reads = pcr_opts.determine_seq_clone_size_error()
        # iterate over clone size and process sequence into reads
        duplicate_i = 0
        # write sequences without error
        for i in range(clone_size - n_mut_reads):
            fw_read, rv_read = sequence_read_pair(allele, insert_len, library_opts)
            reads1_fa.write('>{}:{}/1\n{}\n'.format(base_name, duplicate_i+1, fw_read))
            reads2_fa.write('>{}:{}/2\n{}\n'.format(base_name, duplicate_i+1, rv_read))
            duplicate_i += 1
        # write sequences with PCR error
        if n_mut_reads > 0:
            mut_allele = (allele[0], introduce_pcr_mutation(allele[1], insert_len, library_opts, mutation_opts))
            for i in range(n_mut_reads):
                fw_read, rv_read = sequence_read_pair(mut_allele, insert_len, library_opts)
                reads1_fa.write('>{}:{}/1\n{}\n'.format(base_name, duplicate_i+1, fw_read))
                reads2_fa.write('>{}:{}/2\n{}\n'.format(base_name, duplicate_i+1, rv_read))
                duplicate_i += 1
        # Increate count of used clones
        clone_i += 1
        # Consume remaining reads
        remaining_reads -= clone_size

# Sequence library
def sequence_library(out_dir, popmap_file, alleles_dir, library_opts=LibraryOptions(), mutation_opts=MutationModel(), pcr_opts=PCRDups()):
    # Check output directory
    out_dir = out_dir.rstrip('/')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    elif not os.path.isdir(out_dir): # or not os.path.readable(out_dir):
        sys.exit('oops')
    # Check alleles directory
    alleles_dir = alleles_dir.rstrip('/')
    if not os.path.isdir(alleles_dir):
        sys.exit('oops')
    # generate a sample list from popmap
    samples = []
    for sample in open(popmap_file, 'r'):
        samples.append(sample.strip('\n').split('\t')[0])
    # Define some library variables
    enz = library_opts.renz_1
    # Iterate over samples
    for s_i, sample in enumerate(samples):
        # Extract sample alleles
        alleles_list = load_sample_alleles(sample, alleles_dir, library_opts)
        # Sequence sample
        sequence_sample(sample, out_dir, alleles_list, library_opts, mutation_opts, pcr_opts)
    # TODO parallelize

# Main simulation wrapper
def simulate(genome_dict,
             chrom_len_dict,
             recomb_dict,
             msprime_simulate_args,
             msprime_vcf_dir,
             popmap_file,
             ref_loci_dir,
             master_vcf_dir,
             rad_alleles_dir,
             rad_reads_dir,
             library_opts=LibraryOptions(),
             mutation_opts=MutationModel(),
             pcr_opts=PCRDups(),
             threads=1):
    # Check variables
    assert type(genome_dict) == dict
    assert type(chrom_len_dict) == dict
    assert type(recomb_dict) == dict
    assert isinstance(library_opts, LibraryOptions)
    assert isinstance(mutation_opts, MutationModel)

    # Run msprime; generate variants and popmap
    sim_chromosomes(msprime_vcf_dir, chrom_len_dict, recomb_dict, msprime_simulate_args, popmap_file)
    # Merge and process variants
    merge_vcf(genome_dict, msprime_vcf_dir, master_vcf_dir, mutation_opts)
    # Extract reference RAD loci and generate loci dictionary
    ref_loci_dict = extract_reference_rad_loci(genome_dict, ref_loci_dir, library_opts)
    # Filter RAD variants
    # 1. Generate loci position set for filtering
    loci_pos_set = create_rad_pos_set_dict(ref_loci_dict)
    # 2. Filter
    rad_variants = filter_rad_variants(ref_loci_dict, loci_pos_set, master_vcf_dir)
    # Extract RAD alleles
    extract_rad_alleles(ref_loci_dict, rad_variants, popmap_file, rad_alleles_dir)
    # Sequence samples
    sequence_library(rad_reads_dir, popmap_file, rad_alleles_dir, library_opts, mutation_opts, pcr_opts)

