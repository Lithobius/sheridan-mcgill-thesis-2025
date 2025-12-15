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
# move to folder for data download/processing if needed
cd database12s/

# 5 curate and subset the local database vai multiple filtering parameters

# options for --dereplication-method
# strict: only unique sequences
# single_species: one sequence per species
# unique_species: all unique sequences for each species
crabs --dereplicate --input crabs/20241015_crabs4_pgaout.txt --output crabs/20241015_crabs5_dereplicated.txt --dereplication-method unique_species

# filter
# min and max length
# to be honest, I don't think I care much about this. I'll check to see if its discarding useful stuff
# Min, there's some small segments on NCBI that should match if they align
# Max, I have set to around a mitochondrial genome, but I may need to expand
# --maxns # ambiguous basepairs allowed
# environmental: discard environmental? because we have outgroups, we don't want to do this, we'll filter it in R
# no-species-id: discard 'sp.'? no, we want to permit LCA etc, so don't include this
# rank-na: number of missing taxonomic levels, we're going to allow for every level to be nan so that we can get records that have higher taxonomy but not lower taxonomy, or are just missing some of the taxonomy in NCBI but we can get it back with WoRMS. It seems like some of it is just an issue with ncbi taxonomy but isn't necessarily the sequence itself missing information. So keep it all, we'll fix it in R.
crabs --filter --input crabs/20241015_crabs5_dereplicated.txt --output crabs/20241015_crabs6_filtered.txt --minimum-length 15 --maximum-length 30000 --maximum-n 5 --rank-na 7

# crabs --subset ; can use text file to restrict output
# however, we're doing this in R so we can skip this step I think.
# in the future we may want one to remove known bad NCBI records.
