#!/usr/bin/bash

#SBATCH --account=bgmp                    #REQUIRED: which account to use
#SBATCH --partition=compute               #REQUIRED: which partition to use
#SBATCH --cpus-per-task=4                #optional: number of cpus, default is 1
#SBATCH --mem=16GB                        #optional: amount of memory, default is 4G



read1='/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz'
index1='/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz'
index2='/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz'
read2='/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz'
indexes='/projects/bgmp/shared/2017_sequencing/indexes.txt'

conda activate base

/usr/bin/time -v /projects/bgmp/agwel/bioinfo/Bi622/Demultiplex/Assignment-the-third/demultiplex.py -r1 $read1 -r2 $index1 -r3 $index2 -r4 $read2 -i $indexes