#!/bin/bash

#==============================================================================
#title        :  02_crabs_combine-mifish-ncbifish-outgroups.sh
#description  :  This script combines the output from querying NCBI and extracting mitofish using CRABS.
#author       :  Kate Sheridan
#date         :  20230912
#version      :  0.2.0
#notes        :  requires CRABS, taxonomy file, outputs from previous steps and old versions.
#==============================================================================

# starts in project root
# move to folder for data download/processing
# note here we are not going all the way into crabs folder because we want to use previous references
cd database12s/

# import
## Mitofish
crabs --import --import-format ncbi --input crabs/20241010_mitofish_12s-filter.fasta --names ncbitaxonomy/names.dmp --nodes ncbitaxonomy/nodes.dmp --acc2tax ncbitaxonomy/nucl_gb.accession2taxid --output crabs/20241015_crabs-format_mitofish.txt --ranks 'superkingdom;phylum;class;order;family;genus;species'

## Most recent NCBI fish search
crabs --import --import-format ncbi --input crabs/20241010_12s_fish-ncbi-filter.fasta --names ncbitaxonomy/names.dmp --nodes ncbitaxonomy/nodes.dmp --acc2tax ncbitaxonomy/nucl_gb.accession2taxid --output crabs/20241015_crabs_format_ncbi-12sfish.txt --ranks 'superkingdom;phylum;class;order;family;genus;species'

## Past outgroup search
crabs --import --import-format ncbi --input referencefiles/existing_outgroups/20240212_12s_outgroups-ncbi-filter2.fasta --names ncbitaxonomy/names.dmp --nodes ncbitaxonomy/nodes.dmp --acc2tax ncbitaxonomy/nucl_gb.accession2taxid --output crabs/20241015_crabs_format_ncbi-12soutgroups-past.txt --ranks 'superkingdom;phylum;class;order;family;genus;species'


## Most recent outgroup search
crabs --import --import-format ncbi --input crabs/20241006_12s_outgroups-ncbi-filter2.fasta --names ncbitaxonomy/names.dmp --nodes ncbitaxonomy/nodes.dmp --acc2tax ncbitaxonomy/nucl_gb.accession2taxid --output crabs/20241015_crabs_format_ncbi-12soutgroups-new.txt --ranks 'superkingdom;phylum;class;order;family;genus;species'

#  merge imported files
## Join all imported files
crabs --merge --output crabs/20241015_12s_crabs-merge.txt --uniq --input 'crabs/20241015_crabs-format_mitofish.txt;crabs/20241015_crabs_format_ncbi-12sfish.txt;crabs/20241015_crabs_format_ncbi-12soutgroups-past.txt;crabs/20241015_crabs_format_ncbi-12soutgroups-new.txt'
