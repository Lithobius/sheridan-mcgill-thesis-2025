#!/bin/bash

#==============================================================================
#title        :  02_crabs_combine-mifish-ncbifish-outgroups.sh
#description  :  This script combines the output from querying NCBI and extracting mitofish using CRABS.
#author       :  Kate Sheridan
#date         :  20230912
#version      :  0.1.0
#notes        :  requires CRABS, taxonomy file from 01a.
#==============================================================================

# starts in project root
# move to folder for data download/processing
cd database12s/

# 4 pga
# uses pairwise global alignment to test if
# any of the references just had the primers trimmed out
# this appends to pcr results
# this also adds the taxonomy in the process, elimitating a step from the past pipeline
crabs --pairwise-global-alignment --amplicons crabs/20241015_crabs3_pcrout.txt --input crabs/20241015_12s_crabs-merge.txt --output crabs/20241015_crabs4_pgaout.txt --percent-identity .9 --coverage .9 --forward GTCGGTAAAACTCGTGCCAGC --reverse CATAGTGGGGTATCTAATCCCAGTTTG #--all-start-positions
