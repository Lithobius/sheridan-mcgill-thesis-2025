#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
To eliminate things we already have.
If updating, move a copy of the old fasta into
the existing_outgroups directory and add it to this script.

It takes in fastas and outputs csv to be input into the
R script to make the new list. This can take a 50k+ list
and turn it into 3500. etc.

Author: Kate Sheridan
2024 version 0.1.0
"""

# load-in
import os
import csv
from pyprojroot import here # for 'here' like R

# log-setup
# check logging package for more settings
# I'm mostly using the debug options for development
import logging

LOG_FILENAME = 'outgroups-merge-log.txt'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
logging.info('Debut!')


# set up classes and functions

# read in fasta, write out csv
def fastamatch(raw_fasta, csv2write):
    # open old fasta to read and new fasta to write
    with open(raw_fasta, 'r') as f, \
        open(csv2write, 'a') as out:
        accwriter = csv.writer(out, delimiter = ",")
        accwriter.writerow(["accession"])
        for line in f:
            if line.startswith('>'):
                asvnum = line[1:-1]
                logging.info("found " + asvnum)
                accwriter.writerow([asvnum])
            else:
                pass


# script
if __name__ == "__main__":

    # input FASTA
    fasta = here("./database12s/referencefiles/existing_outgroups/20240212_12s_outgroups-ncbi-filter2.fasta")
    fasta2 = here("./database12s/referencefiles/existing_outgroups/20240212_12s_outgroups-ncbi-filter2.fasta")
    # csv to write out
    new_csv = here('./database12s/referencefiles/existing_outgroups/20241006_outgrouptest.csv')
    # run fasta function
    fastamatch(fasta, new_csv)
    fastamatch(fasta2, new_csv)

    # too long ones
    # input FASTA
    toolong = here("./database12s/referencefiles/existing_outgroups/20240212_12s_outgroups-ncbi-filter2.fasta")
    toolong2 = here("./database12s/referencefiles/existing_outgroups/20240212_12s_outgroups-ncbi-filter2.fasta")
    # csv to write out
    new_csv2 = here('./database12s/referencefiles/existing_outgroups/20241006_outgroup-toolong-test.csv')
    # run fasta function
    fastamatch(toolong, new_csv2)
    fastamatch(toolong2, new_csv2)

# end
logging.info('Fin!')
