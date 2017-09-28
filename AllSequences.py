#
####################################
# Copyright Rahel Frick
# email: frick.rahel@gmail.com
####################################

import os, os.path, re, sys
from Sequence import Sequence
import matplotlib.pyplot as plt
from constants import *
import seaborn as sns; sns.set()
import numpy as np
import pandas as pd


class AllSequences(object):
	'''Handles one folder as downloaded from GATC containing .seq, .fas and .abc files'''
	
	def __init__(self, directory, reference_file, start_site, linker, end_site):

		ref_seq = Sequence(reference_file, start_site, linker, end_site)

		#start_site = ref_seq.sequence[0:6]
		#end_site = ref_seq.sequence[-7:-1]

		# getting start and end indices of linker in reference sequence
		find_linker = re.search(linker, ref_seq.sequence)
		self.start_linker = find_linker.start()
		self.end_linker = find_linker.end()

		self.directory = directory
		self.file_list = []
		for filename in os.listdir(self.directory):
			
			# print filename
			if filename.endswith('.fas'):
				self.file_list.append(os.path.join(os.path.abspath(self.directory), filename))
		self.names = []
		self.mutationlist =[]
		self.aa_sequences= []
		self.bad_sequences = []
		self.mutation_positions = []
		self.mutation_types = []
		self.mutation_types_count = {}
		self.mutation_numbers = []

		#self.no_seq_files = 0

		self.aa_mutationlist =[]
		self.aa_mutation_positions = []
		self.aa_mutation_types = []
		self.aa_mutation_types_count = {}
		self.aa_mutation_numbers = []
		self.stop_codons = []


		for seq in self.file_list:
			#self.no_seq_files += 1
			test_sequence = Sequence(seq, start_site, linker, end_site, reference=ref_seq)
			if test_sequence.bad_sequence == False:

				self.names.append(test_sequence.name)
				self.stop_codons.append(test_sequence.stop_codons)

				self.mutationlist.append(test_sequence.mutationlist)
				self.aa_mutationlist.append(test_sequence.aa_mutationlist)
				self.mutation_numbers.append(test_sequence.mutations)
				
				if test_sequence.truncation == False:
					self.aa_mutation_numbers.append(test_sequence.aa_mutations)
				else:
					self.aa_mutation_numbers.append('NA')

				self.mutation_positions += test_sequence.mutation_positions
				self.aa_mutation_positions += test_sequence.aa_mutation_positions

				self.mutation_types += test_sequence.mutation_types
				self.aa_mutation_types += test_sequence.aa_mutation_types

				self.aa_sequences.append(str(test_sequence.aa_sequence))

			else:
				self.bad_sequences.append(test_sequence.name)

		self.aa_functional_sequences = []
		for item in self.aa_mutation_numbers:
			if item != 'NA':
				self.aa_functional_sequences.append(item)

		#stop codons
		number_of_seq = len(self.names)
		ambers = 0
		opals = 0
		ochres = 0
		for item in self.stop_codons:
			#print item
			if 'amber' in item:
				ambers +=1
			if 'opal' in item:
				opals += 1
			if 'ochre' in item:
				ochres += 1

		#self.amber_ratio = float(ambers)/number_of_seq
		#self.opal_ratio = float(opals)/number_of_seq
		#self.ochre_ratio = float(ochres)/number_of_seq

		#print self.amber_ratio, self.opal_ratio, self.ochre_ratio

		self.no_dna_seq = len(self.names)
		self.no_aa_seq = len(self.aa_functional_sequences)

		#mutation frequencies 
		self.mutation_frequency_dna = np.mean(np.array(self.mutation_numbers))/float(len(ref_seq.sequence))
		self.mutation_frequency_aa = np.mean(np.array(self.aa_functional_sequences))/float(len(ref_seq.aa_sequence))


		self.dna_sequence_length = len(ref_seq.sequence)
		self.aa_sequence_length = len(ref_seq.aa_sequence)
		#print self.dna_sequence_length
		#print self.aa_sequence_length

		for mutation in possible_dna_mutations:
			self.mutation_types_count[mutation] = self.mutation_types.count(mutation)


		#print self.aa_mutation_types		
		for mutation in possible_aa_mutations:
			self.aa_mutation_types_count[mutation] = self.aa_mutation_types.count(mutation)

		self.mean_mutation_number = np.mean(self.mutation_numbers)
		self.stdev_mutation_number = np.std(self.mutation_numbers)
		#print self.names
		#print self.stop_codons

		if self.no_dna_seq == 0:
			sys.exit('\n\nERROR: None of the provided sequences can be analyzed with AnMut. No output will be produced.')


		print '#########################\nWriting output'
		self.write_output()
		print 'plotting mutation distribution over sequence'
		self.plot_mutation_distribution()
		print 'Plotting the distribution of numbers of mutations over all sequences'
		self.plot_mutation_numbers_distribution()
		print 'Plotting mutation types'
		self.plot_mutation_types()
		


	def write_output(self):
		outfile = os.path.join(self.directory, 'sequence_report.txt')
		f = open(outfile, 'w')
		f.write('Please check the following sequences manually:\n')
		for item in self.bad_sequences:
			f.write(item + '\n')
		f.write('\n\n The following sequences (ID along with number of mutations on DNA and aa level) were successfully analyzed:\n')
		for i in range(len(self.names)):
			f.write(self.names[i]+'\t\t\t\t\t')
			f.write('DNA level: %s \t\t\t AA level: %s\n' %(str(self.mutation_numbers[i]), str(self.aa_mutation_numbers[i])))
			#f.write(str(self.mutation_numbers[i]) + '  ' + str(self.aa_mutation_numbers[i]) +'\n')
		f.write('\n\n---------------------------------\nSequence Stats\n---------------------------------\n')
		f.write(' There are on average %f mutations per sequence. Standard deviation is %f' %(self.mean_mutation_number, self.stdev_mutation_number))
		f.write('\nMutation frequency on DNA level: %s %%\nMutation frequncy on AA level: %s %%' %(self.mutation_frequency_dna*100, self.mutation_frequency_aa*100))
		f.write('\n\nPercentage of truncated sequences based on different stop codons:\n')
		#f.write('Amber stops (%s) are contained in %f %% of the sequences' %(stop_codons['amber'], self.amber_ratio*100))
		#f.write('\nOpal stops (%s) are contained in %f %% of the sequences' %(stop_codons['opal'], self.opal_ratio*100))
		#f.write('\nOchre stops (%s) are contained in %f %% of the sequences' %(stop_codons['ochre'], self.ochre_ratio*100))

		f.write('\n\nDetailed information about individual sequences:\n------------------------------------------------------------------\n')
		for i in range(len(self.names)):
			f.write(self.names[i]+'\n')
			f.write('Mutations on DNA level: ')
			f.write(" ".join(self.mutationlist[i]))
			f.write('\nAmino Acid Sequence:\n')
			f.write(self.aa_sequences[i])
			f.write('\n Stop codons in this sequence: %s' %(self.stop_codons[i]))
			f.write('\n\n')

		f.close()


	def plot_mutation_distribution(self):
		plt.clf()
		try:
			bin_max = max(self.mutation_positions)
		except ValueError:
			print "WARNING: No mutations recognized. I cannot plot the distributions of mutations."
			bin_max = 1

		number_of_bins = np.linspace(-0.5, bin_max +0.5, bin_max+2)
		if len(self.mutation_positions) == 0:
			plt.plot([])
		else:
			y, x, _ = plt.hist(self.mutation_positions, bins = number_of_bins, color='#444B6E', linewidth=0)
			plt.axvline(self.start_linker, linewidth=2, color='crimson')
			plt.axvline(self.end_linker, linewidth=2, color='crimson')
			plt.yticks(np.arange(0, max(y)+1, 10))
			plt.title('Mutation positions on DNA level')
			plt.ylim(0, y.max()+1)
			plt.xlim(-0.5, self.dna_sequence_length+1)
			plt.ylabel('Absolute frequency')
			plt.xlabel('Position in Sequence')
			plt.savefig(os.path.join(self.directory, 'mutation_distribution.png'), dpi=300)
			plt.clf()
			try:
				bin_max = max(self.aa_mutation_positions)
			except ValueError:
				bin_max = 1
			number_of_bins = np.linspace(-0.5, bin_max + 0.5, bin_max + 2)
			y, x, _ = plt.hist(self.aa_mutation_positions, bins=number_of_bins, color='#444B6E', linewidth=0)
			plt.axvline(self.start_linker/3, linewidth=2, color='crimson')
			plt.axvline(self.end_linker/3, linewidth=2, color='crimson')
			plt.title('Mutation positions on amino acid level')
			plt.yticks(np.arange(0, self.aa_sequence_length+1, 10))
			plt.ylim(0, y.max()+1)
			plt.xlim(-0.5, self.aa_sequence_length+1)
			plt.ylabel('Absolute frequency')
			plt.xlabel('Position in aa Sequence')
			plt.savefig(os.path.join(self.directory, 'aa_mutation_distribution.png'), dpi=300)		


	def plot_mutation_numbers_distribution(self):
		plt.clf()
		try:
			bin_max = max(self.mutation_numbers)
		except ValueError:
			sys.exit('WARNING: No mutations recognized. I cannot print the distribution of mutation rates.')
		mutation_num_bins = np.linspace(-0.5, bin_max + 0.5, bin_max+2)
		y, x, _ = plt.hist(self.mutation_numbers, bins=mutation_num_bins, histtype='stepfilled', color='#444B6E')
		ax = plt.gca()
		plt.ylim(0, y.max()+1)
		plt.yticks(np.arange(1, max(y)+1, 1.0))
		plt.xticks(np.arange(0, max(x) +1, 10))
		plt.xlim(-0.5, max(self.mutation_numbers)+1)
		plt.title('Mutations per sequence on DNA level')
		plt.ylabel('Absolute frequency')
		plt.xlabel('Number of mutations')
		plt.savefig(os.path.join(self.directory, 'mutation_number_distributions.png'), dpi=300)

		plt.clf()
		try:
			bin_max = max(self.aa_mutation_numbers)
		except ValueError:
			bin_max = 1
		mutation_num_bins = np.linspace(-0.5, bin_max + 0.5, bin_max+2)
		y, x, _ = plt.hist(self.aa_functional_sequences, bins=mutation_num_bins, histtype='stepfilled', color='#444B6E')
		ax = plt.gca()
		plt.ylim(0, y.max()+1)
		plt.yticks(np.arange(1, max(y)+1, 1.0))
		plt.xticks(np.arange(0, max(x) +1, 10))
		plt.xlim(-0.5, max(self.aa_functional_sequences)+1)
		plt.title('Mutations per sequence on amino acid level')
		plt.ylabel('Absolute frequency')
		plt.xlabel('Number of mutations')
		plt.savefig(os.path.join(self.directory, 'aa_mutation_number_distributions.png'), dpi=300)


	def plot_mutation_types(self):
		plt.clf()
		#if len(list(self.mutation_types_count.values())) == 0:
			#print 'WARNING: No mutations recognized. I cannot plot the mutation types.'
			#return None
		ser = pd.Series(list(self.mutation_types_count.values()), index=pd.MultiIndex.from_tuples(self.mutation_types_count.keys()))
		df =ser.unstack().fillna(0)
		df.shape
		ax = sns.heatmap(df, annot=True, cmap='Blues', fmt='g')
		ax.set_axis_bgcolor('white')
		plt.title('Mutation types on DNA level')
		plt.ylabel('Mutate from ...')
		plt.xlabel('Mutate to ...')
		ax.plot()
		plt.savefig(os.path.join(self.directory, 'mutation_types_distribution.png'), dpi=300)

		plt.clf()
		ser = pd.Series(list(self.aa_mutation_types_count.values()), index=pd.MultiIndex.from_tuples(self.aa_mutation_types_count.keys()))
		df =ser.unstack().fillna(0)
		df.shape
		ax = sns.heatmap(df, annot=True, cmap='Blues', fmt='g')
		ax.set_axis_bgcolor('white')
		plt.title('Mutation types on amino acid level')
		plt.ylabel('Mutate from ...')
		plt.xlabel('Mutate to ...')
		ax.plot()
		plt.savefig(os.path.join(self.directory, 'aa_mutation_types_distribution.png'), dpi=300)



