#
####################################
# Copyright Rahel Frick
# email: frick.rahel@gmail.com
####################################

unknown = 'nNX'


def compare_sequences(sequence_position, reference_position):
	'''Takes two characters that are to be compared and returns if the sequence is identical (True) or not (false)
	'''
	if reference_position == sequence_position or reference_position == sequence_position.upper() or sequence_position in unknown:
		return True

	else:
		return False


def align_sequences(sequence, reference, unknown = 'nNX'):

	mutation_positions = []
	mutation_types = []
	mutation_list = []
	for i in range(len(sequence)):
		if compare_sequences(sequence[i], reference[i]) == True:
			pass
		else:
			mutation_positions.append(i+1)
			mutation_types.append((reference[i], sequence[i].upper()))
			mutation = reference[i] + str(i+1) + sequence[i].upper()
			mutation_list.append(mutation)
	mutations = len(mutation_list)
	#print mutations

	return mutation_positions, mutation_types, mutation_list, mutations



def get_all_combinations_from_list(input_list):
	'''takes a list and returns a list of tuples of all possible combinations. 
	Example input: ['A', 'C', 'G']
	Example output: [('A', 'C'), ('A', 'G'), ('C', 'A'), ('C', 'G'), ('G', 'A'), ('G', 'C')]
	'''
	output_list = []

	for item1 in input_list:
		for item2 in input_list:
			if item2 != item1:
				tup = (item1, item2)
				output_list.append(tup)

	return output_list

