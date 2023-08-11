#!/usr/bin/env python

import bioinfo
import argparse
import gzip


def get_args():
    parser = argparse.ArgumentParser(description='program to demultiplex four read files')
    parser.add_argument('-r1', '--read1', help="file containing the first read")
    parser.add_argument('-r2', '--index1', help='file containing index 1 reads')
    parser.add_argument('-r3', '--index2', help='file containing index 2 reads')
    parser.add_argument('-r4', '--read2', help='file containing the second read')
    parser.add_argument('-i', '--known_index', help='tsv containing known indexes')
    return parser.parse_args()

def reverse_complement(seq: str):
    '''Takes a string as input. Returns the reverse complement of the DNA or RNA sequence.'''
    rev_comp = ''
    reverse_seq = seq[::-1]
    for base in reverse_seq.upper(): 
        if base == "A":
            rev_comp += 'T'
        elif base == "T":
            rev_comp += 'A'
        elif base == "G":
            rev_comp += 'C'
        elif base == "C":
            rev_comp += 'G'
        else: 
            rev_comp += 'N'
    return rev_comp

def get_read(fh):
    '''Takes a file handle as input. Reads four lines of FASTQ file and saves each one in the 
    appropriate variable. Returns each variable.'''
    header = fh.readline().strip()
    seq = fh.readline().strip()
    plus = fh.readline().strip()
    q_score = fh.readline().strip()
    return header, seq, plus, q_score

def get_index(fh):
    '''Takes a file handle as input. Reads four lines of FASTQ file and saves only the second line (the sequence line) into
    a variable delineated as the index. Returns the index sequence from the file. '''
    fh.readline().strip()
    index = fh.readline().strip()
    fh.readline().strip()
    fh.readline().strip()
    return index

def check_for_N(index: str):
    '''Takes a string as input. Checks each character for an N. If there is an N in the string, returns True.
    Otherwise, returns False.'''
    for char in index.upper(): 
        if char == "N":
            return True
    else: 
        return False
    
def check_known(index: str, known_indexes: dict):
    '''Takes a string as input. Checks string against every index in inputted dictionary. If there is a match,
     returns True. Else, returns False. '''
    for key in known_indexes:
        if index == key: 
            return True
    else: 
        return False

#Get arguments for read files and file containing known indexes       
args = get_args()

# known_file = '/projects/bgmp/shared/2017_sequencing/indexes.txt'
known_indexes = {}

#open known index file and save each known index in a dictionary
with open(args.known_index, 'r') as input: 
    for line in input: 
        if line == ' ':
            break
        elif line.startswith('sample'):
            continue
        else:
            line = line.strip()
            index = line.split('\t')[4]
            known_indexes[index] = 0

#create a dictionary with indexes as the keys and file handles as the values
files = {}

#populate dictionary with file handles for respective indexes and R1 and R2
for key in known_indexes: 
    files[f'{key}_R1'] = open(f'{key}.R1.fq', 'w')
    files[f'{key}_R2'] = open(f'{key}.R2.fq', 'w')

#assign variables to file handles for unknown and index-hopped files
unknown_R1 = open('unknown_R1.fq', 'w')
unknown_R2 = open('unknown_R2.fq', 'w')
hopped_R1 = open('hopped_R1.fq', 'w')
hopped_R2 = open('hopped_R2.fq', 'w')

#open zipped read files
r1 = gzip.open(args.read1, 'rt')
r4 = gzip.open(args.read2, 'rt')
r2 = gzip.open(args.index1, 'rt')
r3 = gzip.open(args.index2, 'rt')

#initialize counter for unknown indexes
unknown = 0

#initialize dictionaries for matched pairs and hopped pairs
matches = {}
hopped = {}

#initialize counters for total matched pairs and total hopped pairs
total_matches = 0
total_hopped = 0
#total records in file
total_records = 0

while True: 
    #get read from R1 file
    header1, seq1, plus1, q_score1 = get_read(r1)
    #if we're at the end of the file, break out of loop
    if header1 == '':
        break
    #get read from r4 file
    header2, seq2, plus2, q_score2 = get_read(r4)
    #get index from R2 file
    index1 = get_index(r2)
    #get index 2 from R3 file
    index2 = get_index(r3)

    #reverse complement index 2
    rc_index2 = reverse_complement(index2)
    #save index pair into a variable
    index_pair = f'{index1}-{rc_index2}'

    #format output for writing in output files
    output1 = f'{header1} {index_pair}\n{seq1}\n{plus1}\n{q_score1}\n'
    output2 = f'{header2} {index_pair}\n{seq2}\n{plus2}\n{q_score2}\n'

    #check if either index has an N
    #if so, write to unknown file
    if check_for_N(index1) or check_for_N(rc_index2):
        total_records += 1
        unknown += 1
        unknown_R1.write(output1)
        unknown_R2.write(output2)

    #check if either of the indexes are not known
    #if so, write to unknown file
    elif check_known(index1, known_indexes) == False or check_known(rc_index2, known_indexes) == False: 
        total_records += 1
        unknown += 1
        unknown_R1.write(output1)
        unknown_R2.write(output2)

    #check if indexes match
    #if so, write to respective match file 
    elif index1 == rc_index2:
        total_records += 1
        total_matches += 1
        #add instance to dictionary and/or increment counter
        if index_pair in matches: 
            matches[index_pair] += 1
        else:
            matches[index_pair] = 1
        
        files[f'{index1}_R1'].write(output1)
        files[f'{index1}_R2'].write(output2)

    #Otherwise, it must be index-hopped
    #so, write to index-hopped file
    else:
        total_records += 1
        total_hopped += 1 
        #add instance to dictionary or increment counter
        if index_pair in hopped:
            hopped[index_pair] += 1
        else: 
            hopped[index_pair] = 1
        
        hopped_R1.write(output1)
        hopped_R2.write(output2)

#close read files
r1.close()
r2.close()
r3.close()
r4.close()

#close unknown and hopped output files
unknown_R1.close()
unknown_R2.close()
hopped_R1.close()
hopped_R2.close()

#close all matched pair files
for key in files:
    files[key].close()

#initialize variable for percent of reads for each sample
percent = 0
#open tsv file to hold end report
with open("report.md", 'w') as output: 
    #write percent of reads for each sample and amount of times each match pair occurred
    output.write("Match\tCount\tPercentage of Reads in Total Matches\n")
    for key in matches: 
        percent = (matches[key] / total_matches) * 100
        output.write(f'{key}\t{matches[key]}\t{percent}%\n')
    match_percent = 0
    match_percent = (total_matches / total_records) * 100
    output.write(f"Percentage of Matches in Total Records: {match_percent}%\n")
    
    #write amount of times each mismatch occurred and total amount of index hopping
    output.write("\nIndex-Hopped Pair\tCount\n")
    for key in hopped: 
        output.write(f'{key}\t{hopped[key]}\n')
    output.write(f'Total amount of index hopping: {total_hopped}\n')
    hopped_percent = 0
    hopped_percent = (total_hopped / total_records) * 100
    output.write(f'Percentage of Index-Hopping in Total Records: {hopped_percent}%\n')
    output.write(f'\nAmount of Unknown Index Pairs: {unknown}')


    


        

