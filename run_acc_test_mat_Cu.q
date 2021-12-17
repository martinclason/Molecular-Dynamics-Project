#!/bin/bash
#
#SBATCH -J testjob
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
#conda activate /proj/tfya99/software/condaenv
conda activate /home/x_marcl/.conda/envs/tfya99
#conda list

# Setup out dir
#out_dir=out_metals_larger_longer2
out_dir=out_acc_test_Cu_mat
mkdir -p $out_dir
rm $out_dir/*
echo $out_dir

#time ./ale multi m_config_metals.yaml $out_dir -c config_min.yaml
#time ./ale multi m_config_metals.yaml $out_dir -c config_larger_longer.yaml
time ./ale -d $out_dir -c acc_test_mat_Cu.yaml
#time mpirun python3 parallel_mpi_script.py

echo "job completed"
