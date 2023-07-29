#!/usr/bin/env python

import bioinfo

def init_list(lst: list, value: float=0.0) -> list:
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with 101 values of 0.0.'''
    i = 0
    for i in range(0, 101):
        lst.append(value)
        i+=1
    return lst
my_list: list = []
my_list = init_list(my_list)

def populate_list(file: str) -> tuple[list, int]:
    """This function takes a string of a file name. It creates an empty list, opens the given file, and loops through each record in the file.
    It then converts each phred score to its corresponding number and adds it to the empty list of quality scores for each bp.
    It keeps a counter of total lines in the file, and then returns both the array of score sums and the counter."""
    my_list: list = []
    my_list = init_list(my_list)
    i = 0
    with open(file, "r") as fh: 
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

my_list, num_lines = populate_list(file)