#!python

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

import numpy as np
import msprime, sys, argparse, os
# This is for testing purposes
sys.path.insert(0, '/projects/catchenlab/angelgr2/radinitio_package/radinitio_repo/radinitio')
import radinitio as ri

program_name = os.path.basename(__file__)

#
# set command line variables:
p = argparse.ArgumentParser()
p.add_argument('-g', '--genome',     dest='geno',                              help='Path to reference genome (fasta file)')
p.add_argument('-l', '--chrom-list', dest='clist',                             help='File containing a subsample of chromosomes to simulate')
p.add_argument('-o', '--output',     dest='outd',                              help='Path to an output directory where all files will be written')
p.add_argument('-p', '--num-pop',    dest='npop',    type=int, default=2,      help='Number of populations in the island model')
p.add_argument('-s', '--num-sam',    dest='nsam',    type=int, default=10,     help='Number of samples sampled from each population')
p.add_argument('-e', '--enz',        dest='renz',              default='sbfI', help='Restriction enzyme (sbfI, pstI, ecoRI, bamHI, etc.)')
p.add_argument('-c', '--pcr-c',      dest='pcrc',    type=int, default=0,      help='Number of PCR cycles')
p.add_argument('-t', '--threads',    dest='threads', type=int, default=1,      help='Number of threads')

args = p.parse_args()

# Overwrite the help/usage behavior.
p.format_usage = lambda : '''\
{prog} --genome path --chrom-list path --outdir dir --num-pop int --num-sam int --enz str --threads int

Input/Output files:
    -g, --genome:     Path to reference genome (fasta file)
    -l, --chrom-list: File containing a subsample of chromosomes to simulate. Contains one chromosome id per line
    -o, --output:     Path to an output directory where all files will be written

Demographic model (simple island model)
    -p, --num-pop:    Number of populations in the island model            (default = 2)
    -s, --num-sam:    Number of samples sampled from each population       (default = 10)

Library preparation/sequencing:
    -e, --enz:        Restriction enzyme (sbfI, pstI, ecoRI, bamHI, etc.)  (default = 'sbfI')
    -c, --pcr-c:      Number of PCR cycles

Other:
    -t, --threads:  Number of threads
'''.format(prog=program_name)
p.format_help = p.format_usage

# Check required arguments
for required in ['geno', 'clist', 'outd']:
    if args.__dict__[required] is None:
        print('Required argument \'{}\' is missing.\n'.format(required), file=sys.stderr)
        p.print_help()
        sys.exit(1)

#
# Genome options
#
# Generate chromosome set from chromosome list
chrom_list = open(args.clist).read().split()
# Generate genome dictionary and other genome variables
genome_dict = ri.load_genome(args.geno, set(chrom_list))
# Length dictionary
length_dict = dict()
for chrom in chrom_list:
    length_dict[chrom] = len(genome_dict[chrom])
# Recomb dict
rec_dict = dict()
for chrom in chrom_list:
    rec_dict[chrom] = 3e-8

#
# Msprime parameters
#
# General variables
npops = args.npop
ne = 2500
samples = args.nsam
mig_r = 0.001
pops = []
# Population configurations for simple island model
for i in range(npops):
    pops.append(msprime.PopulationConfiguration(sample_size=samples*2, initial_size=ne, growth_rate=0.0))
# In case of single population
msprime_simulate_args = None
if npops == 1:
    msprime_simulate_args = dict(
    mutation_rate=7e-8,
    population_configurations=pops)
else:
    # Migration matrix for simple island model
    m = mig_r / (4 * (npops - 1)) # per generation migration rate
    mig_matrix = [ [ 0 if i == j else m
            for j in range(npops) ]
            for i in range(npops) ]
    # msprime simulate arguments
    msprime_simulate_args = dict(
        mutation_rate=7e-8,
        population_configurations=pops,
        migration_matrix=mig_matrix)

#
# RADinito class options
#
# Set mutation options
muts_opts = ri.MutationModel()
# set library options
library_opts = ri.LibraryOptions(renz_1=args.renz)
# pcr opts
#   Estimate the number of loci for PCR model
n_sequenced_reads = ri.avg_num_reads(genome_dict, library_opts)
#   Create model
pcr_opts = ri.PCRDups(pcr_c=args.pcrc, n_sequenced_reads=n_sequenced_reads)

#
# Path variables
#
outd = args.outd.rstrip('/')
msprime_vcf_dir = '{}/msprime_vcfs'.format(outd)
popmap_file     = '{}/popmap.tsv'.format(outd)
ref_loci_dir    = '{}/ref_loci_vars'.format(outd)
master_vcf_dir  = '{}/ref_loci_vars'.format(outd)
rad_alleles_dir = '{}/rad_alleles'.format(outd)
rad_reads_dir   = '{}/rad_reads'.format(outd)

#
# Main simulation wrapper
#
# Run base simulations
ri.simulate(genome_dict,
            length_dict,
            rec_dict,
            msprime_simulate_args,
            msprime_vcf_dir,
            popmap_file,
            ref_loci_dir,
            master_vcf_dir,
            rad_alleles_dir,
            rad_reads_dir,
            library_opts,
            muts_opts,
            pcr_opts,
            threads=args.threads)


