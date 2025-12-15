#!/bin/bash
#==============================================================================
#title        :  03_crabs_export-blastdb.sh
#description  :  This script outputs the cleaned database into a format that can be used for taxonomic assignment, then processes that format into a local BLAST database. Input - cleaned database from step 02
#author       :  Kate Sheridan
#date         :  20230912
#version      :  0.1.0
#notes        :  requires CRABS, makeblastdb from NCBI.
#==============================================================================

#### NOTE right now it doesn't want to find taxonomy with the database exported in the crabs way but it is fine if I use the old way


# starts in project root
# move to folder for data download/processing
cd database12s/crabs

pwd

# export
# exports databse into a format for taxonomy assignment
# in format chose the one you want based on the program you will use

## options for --export-format
####### There are new formats to test update this! #####

## sintax: >KY305681;tax=d:Eukaryota,p:Chordata,c:Actinopteri,o:Cypriniformes,f:Cyprinidae,g:Barbodes,s:Barbodes_binotatus
## rdp: >KY213961	root;Eukaryota;Chordata;Actinopteri;;Centropomidae;Lates;Lates_japonicus
## qiif: fasta with only accessions, .txt with key to higher taxonomy: KY305681	k__Eukaryota;p__Chordata;c__Actinopteri;o__Cypriniformes;f__Cyprinidae;g__Barbodes;s__Barbodes_binotatus
## dad: >Eukaryota;Chordata;Actinopteri;Cypriniformes;Botiidae;Botia
### Note I don't see accession or species in DAD format
## dads: >KY250421 Oncorhynchus Oncorhynchus_masou
## idt: >Eukaryota;Chordata;Actinopteri;Gadiformes;Gadidae;Gadus;Gadus_macrocephalus
#crabs --export --input 20241015_crabs6_filtered.txt --output blastdb/20241015_12s_crabs.fasta --export-format rdp

# export the database
crabs --export --input 20241015_crabs6_filtered.txt --output blastdb/20241015_12s_crabs --export-format blast-tax

# export a fasta for checking, etc.
## Make DB with fasta
crabs --export --input 20241015_crabs6_filtered.txt --output blastdb_make/20241015_crabs_mifish.fasta --export-format rdp
# makeblastdb from ncbi command line tools
# manual and instructions: https://www.ncbi.nlm.nih.gov/books/NBK569861/
makeblastdb -in blastdb_make/20241015_crabs_mifish.fasta -out blastdb_make/crabs-mifish -title 20241015_crabs-mifish -dbtype nucl -parse_seqids

### Not dereplicated
###### This didn't seem to make much of a difference
## Make DB with fasta

crabs --filter --input 20241015_crabs4_pgaout.txt --output 20241015_crabs6_filtered_nodereplicate.txt --minimum-length 15 --maximum-length 30000 --maximum-n 5 --rank-na 7

crabs --export --input 20241015_crabs6_filtered_nodereplicate.txt --output blastdb_nodereplicate/20241015_crabs_nodereplicate.fasta --export-format rdp
# makeblastdb from ncbi command line tools
# manual and instructions: https://www.ncbi.nlm.nih.gov/books/NBK569861/
makeblastdb -in blastdb_nodereplicate/20241015_crabs_nodereplicate.fasta -out blastdb_nodereplicate/crabs-mifish -title 20241015_crabs-mifish -dbtype nucl -parse_seqids
