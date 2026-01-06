#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script takes the list of MOTUs to reblast and creates a FASTA to query NCBI

Any license info also goes here
Author: "Kate Sheridan"
Version: "0.1.0"
Status: dev
insert copyright, license, additional credits etc if necessary
"""

# module import
# built-in
import os

# common libraries
import csv
import pandas as pd
from pyprojroot import here  # like here in R

# less-known libraries
# own libraries/functions

# log-setup
# check logging module for more settings
# I'm mostly using the debug options for development
import logging

LOG_FILENAME = 'blast-problems-log.txt'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
logging.info('Debut!')


# %% set up general stuff
# fronter to append to all filenames
version = '20241022_'


# make dictionary for asvs and families
# this must be outside the function
## actually this probably could be a list in this case...
## it is a list this time.
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


# body of script
if __name__ == "__main__":


    asvproblems = here(
        './processeddata/peco/2021_2022_2023_edna/20241022_peco-combined_12s_to-reblast2.txt')
    # input FASTA
    fasta = here(
        "./rawdata/peco/fastq/allyears/20241001_peco-combined_12s_post-lulu-motus.fasta")

    fasta_out = here("./rawdata/peco/fastq/allyears/20241022_peco-combined_12s_problems.fasta")

    # filter the fasta file by partner
    fastamatch(asvproblems, fasta, fasta_out)


# don't forget logging.debug('message' or object) periodically


# end
logging.info('Fin!')
