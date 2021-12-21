#!/bin/bash
#
#SBATCH -J materials-test
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
# Must change variables within this box to create submit script.
# Pass name of this_sims_config.yaml to jobname variable below 
# e.g. job_name=this_sims_config in the beginning of this script
# This script will then automatically create a directory 
# called 'this_sims_config_394395' where it will store
# all output and the slurmcopy-394395.out

# IMPORTANT: 
#     Remember to set -n above to minimum processes needed
#     Remember to set -t above to max time before suspending job
#     If running multi instead, comment out applicable lin below Actual job

# output folder will be named to this plus jobid
job_name=testprot

# Only needed if running ale multi, specify multiconfig below
multi_config=m_testprot.yaml
############################################################


# Change this to change config file, defaults to jobname.yaml
normal_config=$job_name.yaml

SBATCH_JOB_NAME=$job_name
# Setup out_dir
out_dir=$job_name-$SLURM_JOB_ID
mkdir -p $out_dir && echo "Created $out_dir"
# Remove potential files in this folder
rm $out_dir/* && echo "Cleared $out_dir"
echo "Storing output in directory: $out_dir"

############################################################
# Actual job
#time ./ale multi $multi_config $out_dir -c $normal_config
time ./ale -d $out_dir -c $normal_config

# Should not be required to run this also since ale multi should call this
#time mpirun python3 parallel_mpi_script.py

echo "job completed"
echo "Will copy this slurm-$SLURM_JOB_ID.out to $out_dir/slurmcopy-$SLURM_JOB_ID.out"
cp slurm-$SLURM_JOB_ID.out $out_dir/slurmcopy-$SLURM_JOB_ID.out
