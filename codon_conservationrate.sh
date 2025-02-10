#!/bin/bash
#SBATCH -t 72:00:00
#SBATCH -p RM-shared
#SBATCH -N 1
#SBATCH --ntasks-per-node=64

module load anaconda3
conda activate myenv
python /ocean/projects/bio200049p/zjiang2/Scripts/spring24/codon_conservationrate.py 
