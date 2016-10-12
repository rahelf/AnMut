from mutant_scFv_analyzer_constants import *
import re
import subprocess
from Bio.Seq import Seq


class Sequence(object):
	'''Handles one single fasta file as obtained from GATC'''

	def __init__(self, filename, reference=''):

		self.filename = filename
		self.name = filename.split('/')[-1].rstrip('.fas')
		f = open(filename)
		
		seq_dat = f.readlines()
		self.raw_sequence = ''

		# DNA level
		self.identifier = seq_dat[0].lstrip('>')[:8].rstrip('\n')
		try:
			self.raw_sequence = seq_dat[1]
		except:
			pass
		self.bad_sequence = False
		self.mutation_positions= []
		self.mutation_types = []
		self.mutationlist = []

		# aa level
		self.aa_sequence = Seq('')
		self.aa_mutation_positions= []
		self.aa_mutation_types = []
		self.aa_mutationlist = []
		self.truncation = True

		# Find start codon in sequnce (including RE sites) and translate
		self.read_sequence()
		self.stop_codons = []

		if self.bad_sequence == False:

			# Compare to reference sequence
			if reference != '':
				self.start_pos = reference.start_pos
				self.translate_sequence()
				self.align_to_reference(reference)
			elif reference == '':
				self.start_pos = self.dna_seq_object.find(start_codon)
				self.translate_sequence()
				print self.sequence[383:446]


			self.codons = [self.sequence[self.start_pos:][i:i+3] for i in range(0,len(self.sequence[self.start_pos:]),3)]
			#print self.codons
			for key in stop_codons.keys():
				if stop_codons[key] in self.codons:
					self.stop_codons.append(key)



	def read_sequence(self):
		try:
			sequence = re.findall('(?<=%s)[A-Z, a-z]{0,}(?=%s)' %(RE_site_1, RE_site_2), self.raw_sequence, re.IGNORECASE)[0]
			self.sequence= RE_site_1 + sequence + RE_site_2
			self.dna_seq_object = Seq(self.sequence)

		except:
			self.bad_sequence = True

	def translate_sequence(self):
		self.productive_sequence = Seq(self.sequence[self.start_pos:])
		self.aa_sequence = self.productive_sequence.translate()

		
	def align_to_reference(self, reference):
		self.mutations = 0
		if not len(self.sequence) == len(reference.sequence):
			self.bad_sequence = True
		else:
			for i in range(len(reference.sequence)):
				if reference.sequence[i] == self.sequence[i] or reference.sequence[i] == self.sequence[i].upper() or self.sequence[i] in 'Nn':
					pass
				else:
					self.mutations += 1
					self.mutation_positions.append(i+1)
					self.mutation_types.append((reference.sequence[i], self.sequence[i].upper()))

					mutation = reference.sequence[i] + str(i+1) + self.sequence[i].upper()
					# print mutation
					self.mutationlist.append(mutation)

		self.truncation = False	
		self.aa_mutations = 0
		if len(self.aa_sequence) != len(reference.aa_sequence):
			self.truncation = True
		else:
			for i in range(len(reference.aa_sequence)):
				if reference.aa_sequence[i] == self.aa_sequence[i] or self.aa_sequence[i] == 'X':
					pass
				else:
					self.aa_mutations +=1
					self.aa_mutation_positions.append(i+1)
					aa_mutation = reference.aa_sequence[i] +str(i+1) +self.sequence[i]
					self.aa_mutationlist.append(aa_mutation)
					self.aa_mutation_types.append((reference.aa_sequence[i], self.aa_sequence[i]))
