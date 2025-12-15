#!/bin/bash

#==============================================================================
#title        :  02_crabs_combine-mifish-ncbifish-outgroups.sh
#description  :  This script combines the output from querying NCBI and extracting mitofish using CRABS.
#author       :  Kate Sheridan
#date         :  20230912
#version      :  0.2.0
#notes        :  requires CRABS, merged database from 02. Updated for crabs 1.0.0
#==============================================================================

# starts in project root
# move to folder for data download/processing
cd database12s/

# 3: in silico pcr
# 12S	MiFish-U, FW:GTCGGTAAAACTCGTGCCAGC, R:CATAGTGGGGTATCTAATCCCAGTTTG
# NOTE: check python version if error
crabs --in-silico-pcr --input crabs/20241015_12s_crabs-merge.txt --output crabs/20241015_crabs3_pcrout.txt --forward GTCGGTAAAACTCGTGCCAGC --reverse CATAGTGGGGTATCTAATCCCAGTTTG --untrimmed crabs/20201015_crabs3_untrimmed.txt --mismatch 6

crabs --in-silico-pcr --input crabs/20241015_12s_crabs-merge.txt --output crabs/20241015_crabs3_pcrout2.txt --forward GTCGGTAAAACTCGTGCCAGC --reverse CATAGTGGGGTATCTAATCCCAGTTTG --untrimmed crabs/20201015_crabs3_untrimmed.txt --mismatch 3
