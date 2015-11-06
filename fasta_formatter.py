'''
Author: 	E. Reichenberger
Date:		9.10.2014

Purpose: Concatenate files where seqeunces are spread across multiple lines.

>G0DGX7Q01D7GVH rank=0000275 x=1608.0 y=667.0 length=174
TTGCTCTCCTTCGAGGGTGCATTAACGCAGACGACCTAGGATCACCGACTGTGTTGTGGT
ACAACTTGACGAGCAACACGTGGATCCTGCTGTATGTTGCACACTCACCTTGTTTAGGAG
AGTAGAATTTCAACATGTAGGGTTACCATGAATTCTTGGTGACTTGGACCGGTT
'''

import glob
import os
import sys
import gzip

arguments = sys.argv
f_name_in = arguments[1] #'NC_008253.fna' 
f_name_out = arguments[2] #'NC_008253.fna' 

outputFile = open(f_name_out, 'wt') #originally was 'wb' but yielded error.

singleLine = ''

with open(f_name_in, 'r') as inputFile: #this approach opens file and closes it when finished. 
	lines = inputFile.readlines()
	for index, line in enumerate(lines):
		line = line.replace('\n', '')
		lines[index] = lines[index].replace('\n', '')

		if lines[index].startswith('>'):
			lines[index] = '?' + lines[index] + '?' #adds ? to beginining of line and adds '>' to end of lines that starts with '>'
		singleLine = singleLine + lines[index]

spliter = singleLine.split('?')

for i in range(len(spliter)):
	if i != 0:
		outputFile.write(spliter[i] + '\n')

outputFile.close()
