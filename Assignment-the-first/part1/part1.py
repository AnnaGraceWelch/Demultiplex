#!/usr/bin/env python

import bioinfo
import argparse
import matplotlib.pyplot as plt
import gzip

def get_args():
    parser = argparse.ArgumentParser(description='program to create per base distribution of quality scores')
    parser.add_argument('-f', '--filename', help="input FASTQ file to create distribution for")
    parser.add_argument('-o', '--output', help='Name of output file without extension')
    parser.add_argument('-l', '--read_length', type=int, help="length of reads in file")
    return parser.parse_args()


def init_list(lst: list, length, value: float=0.0) -> list:
    '''This function takes an empty list and will create a list of the length passed in "length" and populate it with
    the value passed in "value" . If no value is passed, initializes list
    with values of 0.0.'''
    i = 0
    for i in range(length):
        lst.append(value)
        i+=1
    return lst

def populate_list(file: str) -> tuple[list, int]:
    """This function takes a string of a file name. It creates an empty list, opens the given file, and loops through each record in the file.
    It then converts each phred score to its corresponding number and adds it to the empty list of quality scores for each bp.
    It keeps a counter of total lines in the file, and then returns both the array of score sums and the counter."""
    my_list: list = []
    my_list = init_list(my_list, args.read_length)
    i = 0
    with gzip.open(file, "rt") as fh: 
        for line in fh:
            line = line.strip("\n")
            if i%4 == 3:
                j = 0
                for char in line: 
                    score = bioinfo.convert_phred(char)
                    my_list[j] += score
                    j += 1
            i += 1
    return (my_list, i)

args = get_args()

my_list, num_lines = populate_list(args.filename)

num_records = (num_lines/4)
i = 0

with open(f'{args.output}.tsv', 'w') as output:
    output.write(f'Base Pair\tMean Quality Score\n')
    for i in range(len(my_list)): 
        my_list[i] = (my_list[i]/num_records)
        output.write(f'{i}\t{my_list[i]}\n')

x = range(len(my_list))
y = my_list

plt.bar(x, y)
plt.xlabel("Base Pair Position")
plt.ylabel('Mean Quality Score')
plt.title("Per Base Distribution of Average Quality Scores")
plt.savefig(f'{args.output}.png')