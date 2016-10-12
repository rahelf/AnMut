#constants
RE_site_1 = 'CCATGG'
RE_site_2 = 'GCGGCCGC'
#linker = 'AAGCTTTCAGGGAGTGCATCCGCCCCAAAACTTGAAGAAGGTGAATTTTCAGAAGCACGCGTA'

start_codon = 'ATG'

reference_file = '/Users/rahel/uni/scripts-and-templates/Ina_Sequencing/test_sequences/scFv7.fas'
#reference_file = '/Users/rahel/uni/scripts-and-templates/Ina_Sequencing/test/frequency_ref.fas'

# anotation for hist
linker_positions = range(383, 446)


stop_codons = {}
stop_codons['amber'] = 'TAG'
stop_codons['opal'] = 'TGA'
stop_codons['ochre'] = 'TAA'
