# script to generate mock sequencing data to compare to actual sequencing data
# assuming normal distribution of mutations
import numpy.random
from constants import bases
NcoI = 'CCATGG'
NotI = 'GCGGCCGC'


def generate_mock_sequences(wt_sequence_file, mu, sigma, start, end, num_sequences, outdir):
	'''
	The function takes an input wild type sequence file in fasta format,  a mean and standard deviation for number of mutations per sequence, and a number of sequences that are to be generated.
	'''

	# specifying the wild type sequence
	wt_name = wt_sequence_file.split('/')[-1].split('.')[0]
	f = open(wt_sequence_file)
	wt_sequence = f.readlines()[1].rstrip()


	# generate mock sequences and write them to files
	i = 1
	while i <= num_sequences:
		mutant_num = str(i).zfill(4)
		mutant_sequence = make_one_mock_sequence(wt_sequence, mu, sigma, start, end)
		filename = outdir + '/mutant' + mutant_num + '.fas'
		f = open(filename, 'w')
		f.write('>%s\n' %mutant_num)
		f.write(mutant_sequence)
		i+= 1



def make_one_mock_sequence(wt_sequence, mu, sigma, start, end):
	'''
	Takes a wt sequence (string), a mean and standard deviation for how many mutations are required and returns a randomly mutated sequence.
	'''

	# determine number of mutations
	num_mutations = numpy.random.normal(mu, sigma)
	while num_mutations < 0:
		num_mutations = numpy.random.normal(mu, sigma)

	# determine allowed mutation positions (not in RE sites!)
	allowed_positions_for_mutations = wt_sequence[len(start):-len(end)]
	print allowed_positions_for_mutations

	# determine positions of mutations
	positions_for_mutations = list(numpy.random.sample(num_mutations)*len(allowed_positions_for_mutations) + len(start))

	positions_for_mutations = [int(i) for i in positions_for_mutations]
	print positions_for_mutations


	# write sequence
	mutant_sequence = ''
	for i in range(len(wt_sequence)):
		old_base = wt_sequence[i]

		# non-mutated positions stay the same
		if i not in positions_for_mutations:
			mutant_sequence += old_base

		# in mutated positions each of the three other nucleotides has the same chance to be selected
		else:
			other_bases = list(bases)
			other_bases.remove(old_base)
			new_base = numpy.random.choice(other_bases)
			mutant_sequence += new_base
			#print old_base, new_base

	return mutant_sequence

# ---------------------------------------------------------------------------
generate_mock_sequences('/Users/rahel/uni/projects/AnMut/scFv7.fas', 53.6, 20.6, NcoI, NotI, 1000, '/Users/rahel/uni/projects/AnMut/mock_data')
