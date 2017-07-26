#!/usr/bin/env python
#
####################################
# Copyright Rahel Frick
# email: frick.rahel@gmail.com
####################################


'''
Python script to analyze mutant libraries for phage display (or similar)

Dependencies:
    - install anaconda
    - seaborn, pandas, biopython
    - clustalw

Input:
    - Fasta file containing the references (wildtype) sequences
    - strings containing the recognition sites at the beginning and end of the sequences (typically RE sites)

Output:
    - Figures for visualization of mutation frequency, mutation positions, and mutation types
    - Detailed written sequence report containing mutational frequency etc.

Example run:


'''



import argparse, os, sys#, Tkinter
from Sequence import Sequence
from AllSequences import AllSequences
#from mutant_scFv_analyzer_constants import *



# blank variables
ref_file = ''
dir_list = []
start_site = ''
end_site = ''
linker = ''





# commmand line argument parsing
def parse_args():
    ''' Parse command line options.
    '''

    parser = argparse.ArgumentParser(description='This script will compare your mutant library sequences to a wildtype reference and visualize the results.')


    reference_file = parser.add_argument('-ref_file', required=True, help='Please provide a fasta file of your reference sequence. This is usually the mother clone that you used as a template for the mutagenesis.\nPlease make sure the sequence is in fasta format and contains the recognitions sites in the beginning and the end (usually your RE sites used for cloning, like NcoI/NotI)')

    sequence_dirs = parser.add_mutually_exclusive_group()
    sequence_dirs.add_argument('-seq_dir', help='This should be the path to your GATC directory.')
    sequence_dirs.add_argument('-seq_dir_list', help='This should be a textfile containing absolute paths to several GATC directories. Only for advanced users.')

    start_site = parser.add_argument('-start', required=False, help='Please provide the recognition site that precedes the sequence of interest. Usually the 5 prime RE site. Default is the NcoI recognition site.', default='CCATGG')

    end_site = parser.add_argument('-end', required=False, help='Please provide the recognition site that precedes the sequence of interest. Usually the 5 prime RE site. Default is the NotI recognition site.', default='GCGGCCGC')

    linker = parser.add_argument('-linker', required=False, help='If you would like to highlight a specific stretch of your sequence, please copy it in. This could be the linker sequence. It will be visualized in the plots. If you do not want the linker to be visualized, just pass the flag -linker without an argument.', default='AAGCTTTCAGGGAGTGCATCCGCCCCAAAACTTGAAGAAGGTGAATTTTCAGAAGCACGCGTA')

    parser.add_argument('--version', action='version', version='%(prog)s version 0.2, (c) Rahel Frick <frick.rahel@gmail.com>')

    return parser.parse_args()

if __name__=="__main__":
    args = parse_args()
    print '-----------------------------------------------------------------------'
    # making sure the reference file is specified correctly and saving the path

    if os.path.isfile(args.ref_file):
        ref_file = os.path.abspath(args.ref_file)
        print 'Reading the following reference file: ', ref_file
    else: 
        sys.exit('ERROR! Reference file was not recognized. Please provide the correct path to an existing reference file!')


    # making sure the sequencing directories are specified correctly
    if args.seq_dir:
        dir_list = [os.path.abspath(args.seq_dir)]
    elif args.seq_dir_list:
        f = open(args.seq_dir_list)
        for d in f.readlines():
            dir_list.append(os.path.abspath(d))
    print 'Sequence directories: ', dir_list


    # saving  other variables
    start_site = args.start
    end_site = args.end
    linker = args.linker


    print '\nUnderstood the following parameters:'
    print 'start site: ', start_site
    print 'end site: ', end_site
    print 'linker: ', linker
    print '\n(If any of these parameters are not correct, please rerun the program with the correct command line arguments.)'
    print '-----------------------------------------------------------------------'



    for directory in dir_list:
         print 'Analysing sequences in %s' %directory
         S = AllSequences(directory, ref_file, start_site, linker, end_site)




