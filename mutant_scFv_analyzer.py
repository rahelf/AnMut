#!usr/bin/env python
from Sequence import Sequence
from AllSequences import AllSequences
from mutant_scFv_analyzer_constants import *

#Directories = ['/Users/rahel/Dropbox/Ina_Rahel_sequencing/all_seq', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/Organized sequences/1.1 pIII Small-scale Trans./1710172 pIII', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/Organized sequences/1.2 pIX Small-scale Trans/1710172 pIX/', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/Organized sequences/2.1 pIII Primary Trans./1745236 pIII', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/Organized sequences/2.2 pIX Primary Trans./1745236 pIX/', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/Organized sequences/3.1 pIII LV HV/1789147 pIII', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/Organized sequences/3.2 pIX LV HV/1789171 pIX']
#PCR_Dirs = ['/Users/rahel/Dropbox/Ina_Rahel_sequencing/J003 PCR R1', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/J004 PCR R2', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/J004 PCR R3', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/J006 PCR R1', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/J009 PCR R2']
#PCR_Dirs = ['/Users/rahel/Dropbox/Ina_Rahel_sequencing/J003 PCR R1', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/J004 PCR R2']
Directories = ['/Users/rahel/Dropbox/Ina_Rahel_sequencing/V2 Organized sequences/1.1 pIII Small-scale Trans.', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/V2 Organized sequences/1.2 pIX Small-scale Trans', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/V2 Organized sequences/2.1 pIII Primary Trans.', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/V2 Organized sequences/2.2 pIX Primary Trans.', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/V2 Organized sequences/3.1 pIII LV HV', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/V2 Organized sequences/3.1.1 pIII LV', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/V2 Organized sequences/3.1.2 pIII HV', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/V2 Organized sequences/3.2 pIX LV HV', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/V2 Organized sequences/3.2.1 pIX LV', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/V2 Organized sequences/3.2.2 pIX HV', '/Users/rahel/Dropbox/Ina_Rahel_sequencing/V2 all_seq']

test = ['/Users/rahel/Dropbox/Ina_Rahel_sequencing/5 sequences']


def main():
	 for item in Directories:
	 	print 'Analysing sequences in %s' %item
	 	try:
	 		InaSeq = AllSequences(item, reference_file)
	 		print 'done'
	 	except:
	 		print 'failed'
	#InaSeq = AllSequences('/Users/rahel/Dropbox/Ina_Rahel_sequencing/5 sequences', reference_file)
	#print InaSeq.mutation_types

if __name__=="__main__":
	main()


###### To Do
# command line arguments for GATC folder and reference_file!
# global variables allcaps
# self variables arten aus??? --> dictionary
# linker position selbst rauslesen (based on sequence, keine hard gecodeten positionen wo der linker anfaengt und aufhoert)