#!/usr/bin/bash

#SBATCH --account=bgmp                    #REQUIRED: which account to use
#SBATCH --partition=compute               #REQUIRED: which partition to use
#SBATCH --cpus-per-task=4                #optional: number of cpus, default is 1
#SBATCH --mem=16GB                        #optional: amount of memory, default is 4G

conda activate base

/usr/bin/time -v /projects/bgmp/agwel/bioinfo/Bi622/Demultiplex/Assignment-the-first/part1/part1.py -f /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz -o read_4.distribution -l 101