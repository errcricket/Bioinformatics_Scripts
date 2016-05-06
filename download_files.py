'''
Author: 	E. Reichenberger
Date: 	11.24.2015 

Purpose: Extract accession numbers from file (accession.txt). See if file has already been downloaded, and if not, download file to proper directory. Files will be downloaded and renamed to reflect the accession number.

IMPORTANT!!!!! Times are listed for EST, if you are in another time zone, make the proper hour changes in this script 
'''

import os
import os.path
import sys
import re #regular expressions
from Bio import Entrez
import datetime
import time
import glob

arguments = sys.argv
Entrez.email = arguments[1] #email

accession_ids = []
print('Select method for obtaining the accession numbers?\n')
action = '1'
#action = input('1 -- Input Search Terms\n2 -- Use text file\n')

if action == '1':
	print('\nYou will be asked to enter an organism name, a strain name, and keywords.')
	print('It is not necessary to provide a value to each item (you may just hit [ENTER]), but you must provide at least one item.\n')

	#organism = input('Enter the organism you wish to search for (e.g. Escherichia coli [ENTER])\n')
	#strain = input('Enter the strain you wish to search for. (e.g., HUSEC2011 [ENTER])\n')
	#keywords = input('Enter the keywords separated by a comma (e.g., complete genome, contigs, partial [ENTER])\n')
	search_phrase = ''

	organism = 'Escherichia coli'
	strain = ''
	keywords = 'complete genome'
	if ',' in keywords:
		keywords = keywords.split(',')

	ncbi_terms = ['organism', 'strain', 'keyword']
	ncbi_values = [organism, strain, keywords]

	for index, n in enumerate(ncbi_values):
		if index == 0 and n != '':
			search_phrase = '(' + n + '[' + ncbi_terms[index] + '])'
		else:
			if n != '' and index != len(ncbi_values)-1:
				search_phrase = search_phrase + ' AND (' + n + '[' + ncbi_terms[index] + '])'
		if index == len(ncbi_values)-1 and n != '' and type(n) is not list:
			search_phrase = search_phrase + ' AND (' + n + '[' + ncbi_terms[index] + '])'
		if index == len(ncbi_values)-1 and n != '' and type(n) is list:
			for name in n:
				name = name.lstrip()
				search_phrase = search_phrase + ' AND (' + name + '[' + ncbi_terms[index] + '])'
				

	print('Here is the complete search line that will be used: \n\n', search_phrase)

	handle = Entrez.esearch(db='nuccore', term=search_phrase, retmax=1000, rettype='acc', retmode='text')
	result = Entrez.read(handle)
	handle.close()
	#print(result['Count'])
	gi_numbers = result['IdList']

	fetch_handle = Entrez.efetch(db='nucleotide', id=result['IdList'], rettype='acc', retmode='text')
	accession_ids = [id.strip() for id in fetch_handle]
	fetch_handle.close()

if action == '2':
	file_name = input('Enter the name of the file\n')

	with open(file_name, 'r') as input_file:
		lines = input_file.readlines()
	
		for line in lines:
			line = line.replace('\n', '')
			accession_ids.append(line)
#--------------------------------------------------------------------------------------------------------------

#----------------------------------- Make directory to store files --------------------------------------------
new_path = 'Genbank_Files/'
if not os.path.exists(new_path):
    os.makedirs(new_path)

print('You have ' + str(len(accession_ids)) + ' file(s) to download.') #print(accession_ids)

ending='.gb'

files = []
##CHECK IF FILE HAS BEEN DOWNLOADED
for dirpath, dirnames, filenames in os.walk(new_path):
	for filename in [f for f in filenames if f.endswith(ending)]: #for zipped files
		files.append(os.path.join(dirpath,filename))


for f in files:
	f = f.rsplit('/')[-1]
	f = f.replace('.gb', '')
		
	if f in accession_ids:
		ind = accession_ids.index(f)
		accession_ids.pop(ind)

print('')
print('You have ' + str(len(accession_ids)) + ' file(s) to download.')
#--------------------------------------------------------------------------

###############################################################################
#---ACHTUNG--ACHTUNG--ACHTUNG--ACHTUNG--ACHTUNG--ACHTUNG--ACHTUNG--ACHTUNG----#
###############################################################################
# Call Entrez to download files
# If downloading more than 100 files...
# Run this script only between 9pm-5am Monday - Friday EST
# Send E-utilities requests to http://eutils.ncbi.nlm.nih.gov
# Make no more than 3 requests every 1 second.
# Use URL parameter email & tool for distributed software
# NCBI's Disclaimer and Copyright notice must be evident to users of your service. 
#
# Use this script at your own risk. 
# Neither the script author nor author's employers are responsible for consequences arising from improper usage 
###############################################################################


# CALL ENTREZ: Call Entrez to download genbank AND fasta (nucleotide) files using accession numbers.
###############################################################################
start_day = datetime.date.today().weekday() # 0 is Monday, 6 is Sunday
start_time = datetime.datetime.now().time()
print(str(start_day), str(start_time))
print('')

if ((start_day < 5 and start_time > datetime.time(hour=21)) or (start_day < 5 and start_time < datetime.time(hour=5)) or start_day > 5 or len(accession_ids) <= 100 ):
	print('Calling Entrez...')

	for a in accession_ids:
		if ((datetime.date.today().weekday() < 5 and datetime.datetime.now().time() > datetime.time(hour=21)) or 
			(datetime.date.today().weekday() < 5 and datetime.datetime.now().time() < datetime.time(hour=5)) or 
			(datetime.date.today().weekday() == start_day + 1 and datetime.datetime.now().time() < datetime.time(hour=5)) or 
			(datetime.date.today().weekday() > 5) or len(accession_ids) <= 100 ):

			print('Downloading ' + a)

			new_path = 'Genbank_Files/' + a  + '/'
			if not os.path.exists(new_path):
				os.makedirs(new_path)

			handle=Entrez.efetch(db='nucleotide', id=a, rettype='gb', retmode='text', seq_start=0)
			FILENAME = new_path + a + '.gb'
			local_file=open(FILENAME,'w')
			local_file.write(handle.read())
			handle.close()
			local_file.close()

			handle=Entrez.efetch(db='nucleotide', id=a, rettype='fasta', retmode='text') 
			FILENAME =  new_path + a + '.fna'
			local_file=open(FILENAME,'w')
			local_file.write(handle.read())
			handle.close()
			local_file.close()

else:
	print('You have too many files to download at the time. Try again later.')
#--------------------------------------------------------------------------
