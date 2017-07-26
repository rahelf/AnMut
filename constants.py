# constants
#
####################################
# Copyright Rahel Frick
# email: frick.rahel@gmail.com
####################################


from helper import get_all_combinations_from_list

start_codon = 'ATG'

bases = ['A', 'C', 'T', 'G']
aminoacids= ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y' ]

possible_aa_mutations = get_all_combinations_from_list(aminoacids)
possible_dna_mutations = get_all_combinations_from_list(bases)


stop_codons = {}
stop_codons['amber'] = 'TAG'
stop_codons['opal'] = 'TGA'
stop_codons['ochre'] = 'TAA'


allowed_length_limit = 15