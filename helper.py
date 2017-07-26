def align_sequences(sequence, reference, unknown = 'nNX'):

	mutation_positions = []
	mutation_types = []
	mutation_list = []
	for i in range(len(sequence)):
		if reference[i] == sequence[i] or reference[i] == sequence[i].upper() or sequence[i] in unknown:
			pass
		else:
			mutation_positions.append(i+1)
			mutation_types.append((reference[i], sequence[i].upper()))

			mutation = reference[i] + str(i+1) + sequence[i].upper()
			mutation_list.append(mutation)
	mutations = len(mutation_list)
	#print mutations

	return mutation_positions, mutation_types, mutation_list, mutations

