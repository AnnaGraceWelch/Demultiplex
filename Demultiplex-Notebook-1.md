Demultiplex Assignment the First
Anna Grace Welch

-------------
July 27, 2023
-------------

Part 1
============================================================================
1. I used the following bash commands to determine which files contained the reads and which contained the 
indexes:

Looked at beginning of first file: 
zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz | head

First record output:
@K00337:83:HJKJNBBXX:8:1101:1265:1191 1:N:0:1
GNCTGGCATTCCCAGAGACATCAGTACCCAGTTGGTTCAGACAGTTCCTCTATTGGTTGACAAGGTCTTCATTTCTAGTGATATCAACACGGTGTCTACAA
+
A#A-<FJJJ<JJJJJJJJJJJJJJJJJFJJJJFFJJFJJJAJJJJ-AJJJJJJJFFJJJJJJFFA-7<AJJJFFAJJJJJF<F--JJJJJJF-A-F7JJJJ

So R1 contains the first reads from sequencing as the sequence line is longer than a barcode. 

Looked at beginning of second file: 
zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz | head

First record output:
@K00337:83:HJKJNBBXX:8:1101:1265:1191 2:N:0:1
NCTTCGAC
+
#AA<FJJJ

So R2 contains index1 from sequencing as the sequence line is only four bases. 

Looked at beginning of third file: 
zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz | head

First record output: 
@K00337:83:HJKJNBBXX:8:1101:1265:1191 3:N:0:1
NTCGAAGA
+
#AAAAJJF

So R3 contains index2 from sequencing as the sequence line is only four bases.

Looked at beginning of fourth file:
zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz | head

First record output: 
@K00337:83:HJKJNBBXX:8:1101:1265:1191 4:N:0:1
NTTTTGATTTACCTTTCAGCCAATGAGAAGGCCGTTCATGCAGACTTTTTTAATGATTTTGAAGACCTTTTTGATGATGATGATGTCCAGTGAGGCCTCCC
+
#AAFAFJJ-----F---7-<FA-F<AFFA-JJJ77<FJFJFJJJJJJJJJJAFJFFAJJJJJJJJFJF7-AFFJJ7F7JFJJFJ7FFF--A<A7<-A-7--

So R4 contains read 2 from sequencing as the sequence line is much longer than a barcode would be.

2. I used the following bash commands to determine the length of the reads in each file.

First Read:
zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz | grep -A1 "^@" | grep -v "^@" | grep -v "^--" | head -1 | wc -c

Output: 102
Minus the new line character means the length of each read is 101

Second Read: 
zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.g
z | grep -A1 "^@" | grep -v "^@" | grep -v "^--" | head -1 | wc -c

Output: 102
Minus the new line character means the length of each read is 101

First Index: 
zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.g
z | grep -A1 "^@" | grep -v "^@" | grep -v "^--" | head -1 | wc -c

Output: 9
Minus the new line character means the length of each read is 8

Second Index:
zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.g
z | grep -A1 "^@" | grep -v "^@" | grep -v "^--" | head -1 | wc -c

Output: 9 
Minus the new line character means the length of each read is 8


I then created unit test files with 4 reads each. The first reads should have matching index pairs. The second reads have Ns and should therefore go to the unknown files. The third reads should go to index-hopping files. The last reads should go to unknown as the indexes are not in the known list. 

