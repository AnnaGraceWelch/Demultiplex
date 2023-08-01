# Author: <YOU> <optional@email.address>

# Check out some Python module resources:
#   - https://docs.python.org/3/tutorial/modules.html
#   - https://python101.pythonlibrary.org/chapter36_creating_modules_and_packages.html
#   - and many more: https://www.google.com/search?q=how+to+write+a+python+module

'''This module is a collection of useful bioinformatics functions
written during the Bioinformatics and Genomics Program coursework.
'''

__version__ = "0.3"         # Read way more about versioning here:
                            # https://en.wikipedia.org/wiki/Software_versioning

DNA_bases = set("ATGCNatcgn")
RNA_bases = set("AUGCNaucgn")

def convert_phred(letter: str) -> int:
    '''Converts a single character into a phred score'''
    return ord(letter) - 33

def qual_score(phred_score: str) -> float:
    '''Takes a string of phred scores, sums them, and returns the average quality score of the string.'''
    phred_sum = 0
    for score in phred_score: 
        phred_sum += convert_phred(score)
    return phred_sum / len(phred_score)


def validate_base_seq(seq, RNAflag=False):
    '''This function takes a string. Returns True if string is composed
    of only As, Ts (or Us if RNAflag), Gs, Cs. False otherwise. Case insensitive.'''
    return set(seq) <= (RNA_bases if RNAflag else DNA_bases)

def gc_content(DNA):
    '''Returns GC content of a DNA or RNA sequence as a decimal between 0 and 1.'''
    DNA = DNA.upper()
    return (DNA.count("G") + DNA.count("C")) / len(DNA)

def oneline_fasta(r_file, w_file):
    '''Takes a FASTA file as input. Removes wrapping from FASTA file to make each sequence only one line. 
    Returns FASTA file as output with only two lines for each read (header and sequence).'''
    header = seq = ''
    with (open(r_file, 'r') as input, open(w_file, 'w') as output):
        for line in input: 
            line.strip()
            if line.startswith('>') and header == '':
                header = line
            elif line.startswith('>'):
                    output.write(f'{header}\n{seq}\n')
                    header = line
                    seq = ''
            else:
                    seq += line
        output.write(f'{header}\n{seq}\n')
        
def calc_median(lst: list):
    '''Takes a sorted list and returns median value.'''
    length = len(lst)
    if len(lst)%2 == 0:
        mid_pos1 = lst[length//2]
        mid_pos2 = lst[length//2 - 1]
        median = (mid_pos1 + mid_pos2)/2
    else: 
        median = lst[length//2]
    return median



if __name__ == "__main__":
    # tests for validate_base_seq
    assert validate_base_seq("AAA") == True
    assert validate_base_seq("xxx") == False
    # write tests for functions above, Leslie has already populated some tests for convert_phred
    assert convert_phred("I") == 40, "wrong phred score for 'I'"
    assert convert_phred("C") == 34, "wrong phred score for 'C'"
    assert convert_phred("2") == 17, "wrong phred score for '2'"
    assert convert_phred("@") == 31, "wrong phred score for '@'"
    assert convert_phred("$") == 3, "wrong phred score for '$'"
    print("Your convert_phred function is working! Nice job")
    #tests for gc content
    assert gc_content('AATTCCGA') == 0.375
    assert gc_content('ACGT') == 0.5
    assert gc_content("cgcgcgcg") == 1
    #tests for qual_score
    assert qual_score('AAFEFAEE') == 34.75
    assert qual_score('IIIIIII') == 40
    assert qual_score('////!CC@') == 19.375
    assert qual_score('aacc') == 33
    #tests for calc_median
    assert calc_median([1, 4, 7]) == 4
    assert calc_median([34, 35, 36, 37]) == 35.5
    assert calc_median([1, 23, 37, 48, 53]) == 37
    assert calc_median([22, 35, 47, 53]) == 41
