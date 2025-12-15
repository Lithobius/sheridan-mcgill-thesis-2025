#!/bin/bash
#==============================================================================
#title        :  04_crabs_visualizations.sh
#description  :  This script uses the visualization parameters in CRABS to view parameters of the custom database. Input - cleaned database from step 02
#author       :  Kate Sheridan
#date         :  20230912
#version      :  0.1.0
#notes        :  requires CRABS.
#==============================================================================

# starts in project root
# move to folder for data download/processing
cd database12s/crabs

# basic initial visuals
# diversity by taxonomic level
# barplot with bar for # species and # sequences
# this version has taxonomic level: 1 - superkingdom, 2 - phylum, 3 - class, 4 - order, 5 - family, 6 - genus, 7 - species
# because we're using outgroups, it becomes a bit less useful at lower taxonomy
crabs --diversity-figure --input 20241015_crabs6_filtered.txt --output plots/20241015_diversity.png --tax-level 3

# length of sequences, frequency plot
crabs --amplicon-length-figure --input 20241015_crabs6_filtered.txt --output plots/20241015_ampliconlength.png --tax-level 2

# tree
#### requires clustal: https://anaconda.org/bioconda/clustalw
#crabs --phylogenetic-tree --input 20241015_crabs6_filtered.txt --output plots/phylo/ --tax-level 4 --species 'Clupea pallasii'

# i keep getting list index out of range
# no idea what is wrong with this...
#crabs --amplification-efficiency-figure --input 20241015_12s_crabs-merge.txt --amplicons 20241015_crabs6_filtered.txt --output plots/20241015_ampliconefficiency.png --forward GTCGGTAAAACTCGTGCCAGC --reverse CATAGTGGGGTATCTAATCCCAGTTTG --tax-group Gobiidae

# go back to main database folder for this one
cd ..
pwd
# db_completeness
# you have to provide the species names in a txt or as a string separated by +
## NOTE it has to be species level
# gives you summary stats for sp of interest; assesses reference database but also all of NCBI
#output columns
#1 - name of the species of interest
#2 - number of barcodes of species of interest incorporated in the reference database
#3 - number of species in the reference database that share the same genus
#4 - number of species in the genus according to the NCBI taxonomy
#5 - percentage of species in the genus present in the reference database
#6 - number of species in the reference database that share the same family
#7 - number of species in the family according to the NCBI taxonomy
#8 - percentage of species in the family present in the reference database
#9 - list of species sharing the same genus in the reference database
#10 - list of species sharing the same family in the reference database
crabs --completeness-table --input crabs/20241015_crabs6_filtered.txt --output crabs/plots/20241015_completeness.txt --names ncbitaxonomy/names.dmp --nodes ncbitaxonomy/nodes.dmp --species 'Clupea pallasii+Salmo salar'
