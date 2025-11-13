#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filtering eDNA fasta files by whether the MOTU has passed LULU.
 Output is new FASTA with only QCd sequences.

 NOTE the difference with this script is the input is to REMOVE.

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

LOG_FILENAME = 'filterfastalist-log.txt'

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
            # try here because sometimes it gets mad
            # when it can't find the next line
            try:
            # save the sequence
                if line.startswith('>'):
                    seq = next(f)
                    asvnum = line[1:-1]
                    logging.info("found " + asvnum)
                    if asvnum in fastafilter:
                        pass
                    else:
                        ## newline then sequence then newline
                        out.write(">"+asvnum+"\n" \
                        +seq+"\n")
                else:
                    pass
            except:
                pass
    f.close
    out.close


# script

if __name__ == "__main__":

    # input csv for dictionary
    asvlist = here('./rawdata/peco/fastq/allyears/swarm/20251111_peco-combined_12s_removed-motus.csv')
    # input FASTA
    fasta = here('./rawdata/peco/fastq/allyears/swarm/20251111_peco-combined_12s_swarm_clusterreps-motus.fasta')
    new_fasta = here('./rawdata/peco/fastq/allyears/20251111_peco-combined_12s_post-lulu-motus.fasta')
    # run fasta function
    fastamatch(asvlist, fasta, new_fasta)

# end
logging.info('Fin!')
