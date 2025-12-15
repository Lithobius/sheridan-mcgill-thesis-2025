#!/bin/bash
#==============================================================================
#title        :  clustal-align.sh
#description  :  this script aligns the FASTA from the BLAST database made with CRABS to generate an alignment to be trimmed for the amplification efficiency analysis
#author       :  Kate Sheridan
#date         :  20230912
#version      :  0.1.0
#notes        :
#==============================================================================

# starts in project root
# move to folder for data download/processing
cd database12s/crabs

clustalo -i blastdb_make/20241015_crabs_mifish.fasta -o amplificationefficiency/20241028_crabs_mifish_align.fasta -v
|
