#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generating an NCBI search to get taxonomy from list of accession numbers

Author: Kate Sheridan
2022 version 0.1.0
"""

# load-in
from pyprojroot import here # for 'here' like R

# log-setup
# check logging package for more settings
# I'm mostly using the debug options for development
import logging

LOG_FILENAME = 'mitofish-extract-accns-log.txt'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
logging.info('Debut!')


# set up classes and functions
# list of search terms
to_search = []

# read in fasta
def get_terms_fasta(raw_fasta):
    # open old fasta to read and new fasta to write
    with open(raw_fasta, 'r') as f:
        for line in f:
            if line.startswith('>'):
                asvnum = line[1:-1]
                logging.info("found " + asvnum)
                if asvnum not in to_search:
                    to_search.append(asvnum)
                else:
                    pass
            else:
                pass
    #return acc_list

# write accessions to txt
def save_accns(outfile):
    with open(outfile, "w") as out:
        for acc in to_search:
            out.write(acc+"\n")
            logging.info('wrote: '+acc)


# script
if __name__ == "__main__":


    # input FASTA and txt
    mitofish_fasta = here("./database12s/crabs/mitofishdb.fasta")
    # extract accession numbers
    get_terms_fasta(mitofish_fasta)
    # outfile
    search_terms = here("./database12s/crabs/20241010_mitofish-accns.txt")
    save_accns(search_terms)

# end
logging.info('Fin!')
