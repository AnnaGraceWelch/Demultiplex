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
    header = fh.readline().strip()
    seq = fh.readline().strip()
    plus = fh.readline().strip()
    q_score = fh.readline().strip()
    return header, seq, plus, q_score

def get_index(fh):
    fh.readline().strip()
    index = fh.readline().strip()
    fh.readline().strip()
    fh.readline().strip()
    return index

def check_for_N(index: str):
    for char in index.upper(): 
        if char == "N":
            return True
    else: 
        return False
    
def check_known(index: str):
    for key in known_indexes:
        if index == key: 
            return True
    else: 
        return False
        
args = get_args()

# known_file = '/projects/bgmp/shared/2017_sequencing/indexes.txt'
known_indexes = {}

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

files = {}

for key in known_indexes: 
    files[f'{key}_R1'] = open(f'{key}.R1.fq', 'w')
    files[f'{key}_R2'] = open(f'{key}.R2.fq', 'w')


unknown_R1 = open('unknown.R1.fq', 'w')
unknown_R2 = open('unknown.R2.fq', 'w')
hopped_R1 = open('hopped.R1.fq', 'w')
hopped_R2 = open('hopped.R2.fq', 'w')

r1 = gzip.open(args.read1, 'rt')
r4 = gzip.open(args.read2, 'rt')
r2 = gzip.open(args.index1, 'rt')
r3 = gzip.open(args.index2, 'rt')

unknown = 0
matches = {}
hopped = {}

while True: 
    header1, seq1, plus1, q_score1 = get_read(r1)
    if header1 == '':
        break
    header2, seq2, plus2, q_score2 = get_read(r4)
    index1 = get_index(r2)
    index2 = get_index(r3)

    rc_index2 = reverse_complement(index2)
    index_pair = f'{index1}-{rc_index2}'
    output1 = f'{header1} {index_pair}\n{seq1}\n{plus1}\n{q_score1}\n'
    output2 = f'{header2} {index_pair}\n{seq2}\n{plus2}\n{q_score2}\n'

    if check_for_N(index1) or check_for_N(rc_index2):
        unknown += 1
        unknown_R1.write(output1)
        unknown_R2.write(output2)

    elif check_known(index1) == False or check_known(rc_index2) == False: 
        unknown += 1
        unknown_R1.write(output1)
        unknown_R2.write(output2)

    elif index1 == rc_index2:
        if index_pair in matches: 
            matches[index_pair] += 1
        else:
            matches[index_pair] = 1
        
        files[f'{index1}_R1'].write(output1)
        files[f'{index1}_R2'].write(output2)

    else:
        if index_pair in hopped:
            hopped[index_pair] += 1
        else: 
            hopped[index_pair] = 1
        
        hopped_R1.write(output1)
        hopped_R2.write(output2)


r1.close()
r2.close()
r3.close()
r4.close()

unknown_R1.close()
unknown_R2.close()
hopped_R1.close()
hopped_R2.close()
for key in files:
    files[key].close()

        
with open("matching_count.tsv", 'w') as output: 
    output.write("Match\tCount\n")
    for key in matches: 
        output.write(f'{key}\t{matches[key]}\n')

with open("hopped_count.tsv", 'w') as output: 
    output.write("Index-Hopped Pair\tCount\n")
    for key in hopped: 
        output.write(f'{key}\t{hopped[key]}\n')


print(unknown)

#percentage of reads from each sample
#overall amount of index swapping

    


        

