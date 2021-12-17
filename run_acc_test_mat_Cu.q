#!/bin/bash
#
#SBATCH -J change_me_to_whatever_the_config_is_named_but_without_.yaml
#SBATCH -A liu-compute-2021-30
#SBATCH -t 03:00:00
#SBATCH -n 2
#SBATCH --mail-type=ALL
#
export NSC_MODULE_SILENT=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS=1

module load openmpi/.4.0.5-gcc-2020b-eb
module load Anaconda/2020.07-nsc1
conda activate tfya99
#conda list

############################################################
########################## README ##########################
# Pass name of this_sims_config.yaml to jobname -J 
# e.g. -J this_sims_config in the beginning of this script
# This script will then automatically create a directory 
# called 'this_sims_config_394395' where it will store
# all output and the slurmcopy-394395.out
############################################################

# Setup out_dir
out_dir=$SBATCH_JOB_NAME_$SLURM_JOB_ID
mkdir -p $out_dir && echo "Created $out_dir"
# Remove potential files in this folder
rm $out_dir/* && echo "Cleared $out_dir"
echo "Storing output in directory: $out_dir"

#time ./ale multi m_config_metals.yaml $out_dir -c config_min.yaml
#time ./ale multi m_config_metals.yaml $out_dir -c config_larger_longer.yaml
time ./ale -d $out_dir -c $SBATCH_JOB_NAME.yaml
#time mpirun python3 parallel_mpi_script.py

echo "job completed"
echo "Will copy this slurm-$SLURM_JOB_ID.out to $out_dir/slurmcopy-$SLURM_JOB_ID.out"
cp slurm-$SLURM_JOB_ID.out $out_dir/slurmcopy-$SLURM_JOB_ID.out
