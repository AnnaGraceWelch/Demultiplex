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
    parser.add_argument('-m', '--library', help="name of library/file and R1/R2 to put on quality distribution plot", required=True)
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
    #initialize list
    my_list: list = []
    #fill list with 0's to start
    my_list = init_list(my_list, args.read_length)
    #initialize counter for each line in file
    i = 0
    #open file 
    with gzip.open(file, "rt") as fh: 
        for line in fh:
            line = line.strip("\n")
            #if we've reached quality score line
            if i%4 == 3:
                # initialize counter for each quality score in line
                j = 0
                for char in line: 
                    # compute quality score 
                    score = bioinfo.convert_phred(char)
                    #add quality score to running sum for that position
                    my_list[j] += score
                    j += 1
            i += 1
    return (my_list, i)

args = get_args()

#populate list with quality scores, and get number of lines in file
my_list, num_lines = populate_list(args.filename)

# calculate number of records 
num_records = (num_lines/4)
i = 0


with open(f'{args.output}.tsv', 'w') as output:
    output.write(f'Base Pair\tMean Quality Score\n')
    #for each base pair, calculate mean quality score for that position
    for i in range(len(my_list)): 
        my_list[i] = (my_list[i]/num_records)
        #write mean quality score to output file
        output.write(f'{i}\t{my_list[i]}\n')

x = range(len(my_list))
y = my_list

#plot bar chart of distribution of mean quality scores
plt.bar(x, y)
plt.xlabel("Base Pair Position")
plt.ylabel('Mean Quality Score')
plt.title(f'{args.library} Mean Quality Score Distribution')
#save graph as png
plt.savefig(f'{args.output}.png')