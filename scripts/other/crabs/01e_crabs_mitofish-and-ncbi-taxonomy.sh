#!/bin/bash

#==============================================================================
#title        :  01d_crabs_mitofish-and-taxonomy.sh
#description  :  This script uses crabs to download mitofish and the NCBI taxonomy file. Note this taxonomy file is required for future steps of taxonomy assignment, and sometimes updates from NCBI.
#author       :  Kate Sheridan
#date         :  20230912
#version      :  0.2.0
#notes        :  requires CRABS. Updated 16 Oct 2024 for crabs 1.0.0
#==============================================================================

# starts in project root
# move to folder for data download/processing
cd database12s/crabs

# 1: db_download
# crabs can download from several databases

# mitofish db is just all of mitofish
crabs --download-mitofish --output mitofishdb_2024oct.fasta

# taxonomy
# This file needs to be downloaded if we use
# NCBI etc data, even a custom database
crabs --download-taxonomy --output ncbitaxonomy
