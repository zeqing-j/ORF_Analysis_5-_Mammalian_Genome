#!/bin/bash
#SBATCH -t 24:00:00
#SBATCH -p RM-shared
#SBATCH -N 1
#SBATCH --ntasks-per-node=64

module load python
module load anaconda3
conda activate myenv
python /ocean/projects/bio200049p/zjiang2/Scripts/spring24/find_greater_50nt_UTR.py
