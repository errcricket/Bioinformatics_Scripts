'''
Author:	E. Reichenberger
Date:		4.15.2016

Purpose: Concatenate files where sequences are spread across multiple lines. If the input file is example.fa, one of the output files will be example_formatted.fa. This file will contain all formatted sequences in a single file called example_formatted.fa. This script will also output each individual (formatted) sequences to its own unique file. If example.fa has 40 sequences in it, there will be 40 output files (e.g., example_1.fa, example_2.fa, ...example_40.fa.

Call: python format_file_splitter.py file_name.fa
'''

import glob
import os
import sys
import gzip

arguments = sys.argv
fileName = arguments[1] #'NC_008253.fna' 

extension = os.path.splitext(fileName)[1]
newExtension = '_formatted' + extension

fileOut = fileName.replace(extension, newExtension)
outputFile = open(fileOut, 'wt') #originally was 'wb' but yielded error.

singleLine = ''

with open(fileName, 'r') as inputFile: #this approach opens file and closes it when finished. 
	lines = inputFile.readlines()
	for index, line in enumerate(lines):
		line = line.replace('\n', '')
		lines[index] = lines[index].replace('\n', '')

		if lines[index].startswith('>'):
			lines[index] = '?' + lines[index] + '?' #adds ? to beginining of line and adds '>' to end of lines that starts with '>'
		singleLine = singleLine + lines[index]

spliter = singleLine.split('?')

count = 0
for i in range(len(spliter)):
	if i != 0:
		if spliter[i].startswith('>'):
			count+=1
			newExtension = '_' + str(count) + extension
			newFile = fileName.replace(extension, newExtension)
			with open(newFile, 'w') as outputFile2: #output individual sequence to unique file
				outputFile2.write(spliter[i] + '\n')
				outputFile2.write(spliter[i+1] + '\n')
			#print(i, spliter[i], newExtension)
		outputFile.write(spliter[i] + '\n')

outputFile.close()
