#!/bin/bash
#
#SBATCH -J testjob
#SBATCH -A liu-compute-2021-30
#SBATCH -t 00:05:00
#SBATCH -N 1
#SBATCH --exclusive
#
export NSC_MODULE_SILENT=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS=1

module load openmpi/.4.0.5-gcc-2020b-eb
module load Anaconda/2020.07-nsc1

conda activate my-md-env
#conda list
time ./ale multi m_config.yaml out -c test/config_extra_short.yaml
#time mpirun python3 parallel_mpi_script.py

echo "job completed"
