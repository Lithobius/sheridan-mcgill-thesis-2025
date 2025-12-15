#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filtering mitofish fasta file by whether the accession contains 12S / whole mitochondrial genome / 12S-adjacent genes. Output is new FASTA with only relevant sequences.

Author: Kate Sheridan
2022 version 0.1.0
"""

# load-in
import os
import csv
from pyprojroot import here # for 'here' like R

# log-setup
# check logging package for more settings
# I'm mostly using the debug options for development
import logging

LOG_FILENAME = 'mitofish-filterfastalist-log.txt'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
logging.info('Debut!')

# global
asvlist = []

# read in fasta, sort, write out

def fastamatch(list_in, fasta_in, fasta_out):
    fastafilter = open(list_in,).read().splitlines()
    logging.info(fastafilter)
    # open old fasta to read and new fasta to write
    with open(fasta_in, 'r') as f, \
        open(fasta_out, 'w') as out:
        for line in f:
            # save the sequence
            seq = next(f)
            if line.startswith('>'):
                asvnum = line[1:-1]
                logging.info("found " + asvnum)
                if asvnum in fastafilter:
                    # writes >ASV2_Embiotocidae
                    ## the "{!s}\n".format() makes the value a string
                    ## newline then sequence then newline
                    out.write(">"+asvnum+"\n" \
                    +seq+"\n")

                else:
                    pass
            else:
                pass
    f.close
    out.close


# script

if __name__ == "__main__":

    # input list of accessions that passed QC
    asvlist = here('./database12s/crabs/20241010_mitofish_12s.txt')
    # input FASTA
    fasta = here('./database12s/crabs/mitofishdb.fasta')
    new_fasta = here('./database12s/crabs/20241010_mitofish_12s-filter.fasta')
    # run fasta function
    fastamatch(asvlist, fasta, new_fasta)

# end
logging.info('Fin!')
