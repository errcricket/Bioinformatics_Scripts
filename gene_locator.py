'''
Author:	E. Reichenberger	
Date:		10.29.2015
Purpose: If given a genome and a list of genes, search for genes in genome.

Ex. python gene_locator.py genes_formatted.fa reference_genome.fa  #Note: run fasta_formatter.py and check for .
'''

import os
import sys
import gzip

arguments = sys.argv
geneFile = arguments[1]
genomeFile = arguments[2]
kmer_searchFile = ''

if len(arguments) > 3:
	kmer_searchFile = arguments[3]

#######################################DEFINITIONS###################################################
##REMOVE ITEMS: Remove items from string.
def remove_items(string):
	remove_list = ['\n', '\r', '\'', '[', ']']
	for r in remove_list:
		if r in string:
			string = string.replace(r, '')
	return string


##ENTER FUNCTION?: Check user input.
def get_userInput(userInput):
	userInput = userInput.lower()
	if userInput.startswith('y'):
		return 'yes'
#------------------------------------------------------------------------------------------


##########################################################################################
##GENES: Get list of genes into dictionary
genes_dic = {} #key = gene name, value = gene sequence

with open(geneFile, 'r') as inputFile:
	lines = inputFile.readlines()
	
	for index, line in enumerate(lines):
		line = remove_items(line)

		if line.startswith('>'): 
			gene_name = line.strip('>').split(' ')[0] #shorten header to gene name only
			if gene_name not in genes_dic:
				genes_dic[gene_name] = '' 
			genes_dic[gene_name] = str(remove_items(lines[index+1])) #keeping this indented => no index out of bounds errors
#------------------------------------------------------------------------------------------



##REFERENCE GENOME: Get reference genome into an object.
##########################################################################################
genome_seq = ''

with gzip.open(genomeFile, 'rb') as inputFile:
	inputFile.readline()
	genome_seq = str(remove_items(inputFile.readlines())) #leave str, else len(genome_seq) = 1
	genome_seq = remove_items(genome_seq)  #need to run this twice for some reason
	#genome_seq = genome_seq[0:3115] #for current practice, shorten genome_seq length
#------------------------------------------------------------------------------------------


##BUILD K-MER DICTIONARY: Create list of all k-mers where each entry contains kmer list w/ length of gene
# Very slow process -- will save kmers for specific gene to kmer-named file
##########################################################################################
get_kmers = raw_input('\nDo you need to compile a list of all possible kmers? [Y/N ENTER]\n')
kmer_response  = get_userInput(get_kmers)

if kmer_response == 'yes':
	
	kmer_dic = {} #each dictionary value is an array containing all kmers where length = len(gene_dic[key]) 
		
	for g in genes_dic:
		kmer_dic[g] = []
		window_length = len(genes_dic[g]) #print(g, window_length)
		newFile = g + '_kmerList.txt'
		
		with open(newFile, 'w') as kmerFile:
			for index, s in enumerate(genome_seq):	
				if index < len(genome_seq) - window_length + 1:
					if genome_seq[index:index+window_length] not in kmer_dic[g]:
						kmerFile.write(genome_seq[index:index+window_length] + '\n')
						#kmer_dic[g].append(genome_seq[index:index+window_length])
#------------------------------------------------------------------------------------------


##K-MER SEARCH: Search k-mers for gene matches (in || by gene)
# This should be run organized to parse through gene-specific kmers in parallel
##########################################################################################
gene_name = kmer_searchFile.split('_')[0]

keepers = []
acme_list = []
with open(kmer_searchFile, 'r') as inputFile:
	lines = inputFile.readlines()
	for line in lines:	
		acme_list.append(line.replace('\n', ''))
		line = line.replace('\n', '')
		if line == genes_dic[gene_name]:
			keepers.append(line)

print(keepers)
#for g in genes_dic:
#	print(g)

kmer_list = ['ydeO_K12_kmerList.txt.gz', 'emrY_kmerList.txt.gz', 'ydeP_kmerList.txt.gz', 'emrK_kmerList.txt.gz', 'yhiU_mdtE_kmerList.txt.gz', 'yegE_kmerList.txt.gz', 'omrB_kmerList.txt.gz', 'yegR_kmerList.txt.gz', 'omrA_kmerList.txt.gz', 'yhiE_gadE_kmerList.txt.gz', 'yegZ_kmerList.txt.gz', 'cyclic-di-GMP_phosphodiesterase_kmerList.txt.gz', 'rprA_kmerList.txt.gz', 'yhiV_mdtF_kmerList.txt.gz', 'yciR_salm_kmerList.txt.gz', 'yfdX_kmerList.txt.gz', 'gmr_kmerList.txt.gz', 'gcvB_kmerList.txt.gz', 'yfdV_kmerList.txt.gz', 'cpxA_kmerList.txt.gz', 'yhiD_kmerList.txt.gz', 'yhiF_kmerList.txt.gz', 'yciR_EDL933_kmerList.txt.gz', 'arcZ_kmerList.txt.gz', 'mcaS_kmerList.txt.gz', 'csrB_kmerList.txt.gz', 'csrC_kmerList.txt.gz', 'yedR_kmerList.txt.gz']

#------------------------------------------------------------------------------------------
##K-MER Search: Search all kmers for match (Note: for gene yegE search among kmers of len(yegE_gene)), keep matches
#------------------------------------------------------------------------------------------
'''
keepers = {}

for g in genes_dic:
	#print(g, genes_dic[g])
	keepers[g] = []

	for kmer in kmer_dic[g]:
		#print(kmer)
		if kmer == genes_dic[g]:
			keepers[g].append(kmer)
			#keepers[g].append(kmer_dic[g])
		#print(mer)
		#if mer in kmer_dic[g] and mer_dic[g] not in keepers:
		#if genes_dic[g] in kmer_dic[g] and mer_dic[g] not in keepers:

#print(keepers['omrB'][0])
#print(len(keepers))
with open('test', 'w') as output:
	for k in keepers:
		output.write(k + '\n')
print(keepers)
'''
	
#print(kmer_dic['omrB'][0])
#for k in kmer_dic:
#	if kmer_dic[k] in 
#	for n in genes_dic[k]:
#		x = 2#print(n, genes_dic[k]) 
			#print(genome_seq[index:index+window_length])

#				kmer_dic[genome_seq[index:index+window_length]] = 0
#			kmer_dic[genome_seq[index:index+window_length]] = kmer_dic[genome_seq[index:index+window_length]] + 1

#print(kmer_dic)
