#!/bin/bash -l
## NOTE the -l flag!

## Name of the job -You'll probably want to customize this
#SBATCH -J test-history-analyze

## Use the resources available on this account
#SBATCH -A loop

## Standard out and Standard Error output files 
#SBATCH -o log/%J.o
#SBATCH -e log/%J.e

## To send mail for updates on the job
#SBATCH --mail-user=zxyvse@rit.edu
#SBATCH --mail-type=ALL

## Request 3 Days, 5 Hours, 5 Minutes, 3 Seconds run time MAX, 
## anything over will be KILLED
#SBATCH -t 3-03:05:03

## Put in tier3 partition for testing small jobs, like this one
## But because our requested time is over 4 day, it won't run, so
## use any tier you have available
#SBATCH -p tier3

## Request 1 core for one task, note how you can put multiple commands
## on one line
#SBATCH -n 1 -c 1

## Job memory requirements in MB
#SBATCH --mem=16G

## Job script goes below this line

## Make the log directory for standard out and standard error
mkdir -p log
## Load modules with spack
spack load py-pytest
spack load py-gitpython
spack load py-pandas
## Execute target code
python3 tha.py https://github.com/hil-se/auto_test_py

