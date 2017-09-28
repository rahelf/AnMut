#from AnMut import *
#
####################################
# Copyright Rahel Frick
# email: frick.rahel@gmail.com
####################################

import re
from constants import *
import subprocess
from Bio.Seq import Seq
import os.path
from helper import align_sequences


class Sequence(object):
	'''Handles one single fasta file as obtained from GATC'''

	def __init__(self, filename, start_site, linker, end_site, reference=''):

		print '--------------------------------------'
		self.filename = filename
		self.name = os.path.split(filename)[-1].rstrip('.fas')
		f = open(filename)

		seq_dat = f.readlines()
		self.raw_sequence = ''

		# extract identifier and raw sequence from the fas file (DNA level)
		self.identifier = seq_dat[0].lstrip('>').rstrip('\n')
		try:
			self.raw_sequence = seq_dat[1]
		except:
			pass
		#print 'Sequence %s has a length of %i bp.' %(self.identifier, len(self.raw_sequence))


		# Initiate empty lists for mutation positions, mutation types and fully specified mutations (DNA level)
		self.bad_sequence = False
		self.mutation_positions= []
		self.mutation_types = []
		self.mutationlist = []
		
		# Make empty sequence object for aa sequece
		self.aa_sequence = Seq('')

		# Initiate same empty lists to keep track of mutations but this time on aa level.
		self.aa_mutation_positions= []
		self.aa_mutation_types = []
		self.aa_mutationlist = []

		# By default I assume a sequence is not truncated
		self.truncation = False
		#self.truncation = True

		# Find start and end sites in sequence. Makes a clean self.sequence including the RE sites. 
		self.read_sequence(start_site, linker, end_site)
		self.stop_codons = []

		#print 'Identifier: %s\nSequence: %s' %(self.identifier, self.raw_sequence)


		#print self.bad_sequence
		if self.bad_sequence == False:

			# Compare to reference sequence if there is a reference sequence. Now we want the same start position as in the reference sequence and translate from here.
			if reference != '':
				self.start_pos = reference.start_pos
				self.translate_sequence()
				# We also want to align the test sequence to the reference sequence
				self.align_to_reference(reference)

			# If this is the reference sequence itself (aka there is no other given reference sequence) we want to determine the start position at a start codon. And then translate the sequence from here.
			elif reference == '':
				self.start_pos = self.dna_seq_object.find(start_codon)
				self.translate_sequence()

			#make a list of all codons in a sequence to later check for stop codons.
			self.codons = [self.sequence[self.start_pos:][i:i+3] for i in range(0,len(self.sequence[self.start_pos:]),3)]
			#print self.codons

			# now checking for stop codons and making a list of the ones found in the sequence.
			for key in stop_codons.keys():
				if stop_codons[key] in self.codons:
					self.stop_codons.append(key)



	def read_sequence(self, start_site, linker, end_site):
		'''Takes a start site, linker site, and end_site and returns a cleaned self.sequence and a Seq object of it (self.dna_seq_object).
		'''

		# Try to find the sequence between the start and end site. upper or lower case letters are accepted in the start and end sites.
		try:
			sequence = re.findall('(?<=%s)[A-Z, a-z]{0,}(?=%s)' %(start_site, end_site), self.raw_sequence, re.IGNORECASE)[0]
			self.sequence= start_site + sequence + end_site
			self.dna_seq_object = Seq(self.sequence)

		# If a sequence cannot be identified based on the given start and end sites, it is a bad sequence.
		except:
			self.bad_sequence = True


	def translate_sequence(self):

		print 'Translating sequence %s...' %self.filename
		#the productive sequence starts at the start position. This is a start codon in the reference but could be something else in the mutants.
		self.productive_sequence = Seq(self.sequence[self.start_pos:])

		# using Biopython to translate the productive part of the sequence
		self.aa_sequence = self.productive_sequence.translate()

		
	def align_to_reference(self, reference):

		print 'Aligning sequence %s...' %self.filename
		
		# Does the test sequence have the same length as the reference sequence?
		diff = len(self.sequence) - len(reference.sequence)

		# these are sequences that seem to have a frameshift mutation or truncation or by more than the allowed length limit (internal RE site or sequencing problem)
		if not diff == 0:
			self.bad_sequence = True
			print 'The sequence has an unexpected length and probably has an out of frame mutation, truncation or was sequenced incompletely.'
		
		# these are sequences with same length as reference
		elif len(self.sequence) == len(reference.sequence):
			print 'The sequence has the expected length and can be analyzed normally.'
	
			self.mutation_positions, self.mutation_types, self.mutation_list, self.mutations = align_sequences(self.sequence, reference.sequence)

			
		#self.truncation = False	

		if len(self.aa_sequence) != len(reference.aa_sequence):
			self.truncation = True
		else:
			self.aa_mutation_positions, self.aa_mutation_types, self.aa_mutationlist, self.aa_mutations = align_sequences(self.aa_sequence, reference.aa_sequence)



