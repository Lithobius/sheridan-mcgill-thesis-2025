#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sequence table format for swarm
take two
I need to make it:
>asv#_abundance
actgsequenceactg

Author: Kate Sheridan
2022 version 0.1.0
"""

# load-in
import os
import re
import pandas as pd
from pyprojroot import here # for 'here' like R

# log-setup
# check logging package for more settings
# I'm mostly using the debug options for development
import logging

LOG_FILENAME = 'swarmformat-log.txt'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
logging.info('Debut!')


# set up classes and functions
asvdic2 = {}
# read in fasta, sort, write out
def asv_abund(asv_in):
    asv_tab = pd.read_csv(asv_in, sep = '\t')
    # modify to long format; melt
    asv_tab_long = pd.melt(asv_tab, id_vars=['row_names'], var_name=["asv"])
    asv_tab_long = asv_tab_long.loc[asv_tab_long['value'] > 0]
    asv_tab_long = asv_tab_long.drop(['row_names'], axis=1)
    asv_combine = asv_tab_long.groupby('asv')['value'].sum('value').reset_index()
    asvdic2 = asv_combine.set_index(['asv']).to_dict(orient='dict')['value']
    return(asvdic2)


def asv_toswarm(asv_dict, asv_fasta, swarm_fasta):
    # open old fasta to read and new fasta to write
    with open(asv_fasta, 'r') as f, \
        open(swarm_fasta, 'w') as out:
        for line in f:
            # save the sequence
            seq = next(f)
            if line.startswith('>'):
                asvnum = line[1:-1]
                logging.info("found " + asvnum)
                if asvnum in asv_dict:
                    # writes >ASV2_Embiotocidae
                    ## the "{!s}\n".format() makes the value a string
                    ## newline then sequence then newline
                    out.write(">"+asvnum+"_"+"{!s}\n".format(asv_dict[asvnum])\
                    +seq+"\n")
                    logging.info('wrote ' + asvnum)
                else:
                    pass
            else:
                pass

# script

if __name__ == "__main__":

    # sequence matrix; columns sequences rows samples values reads
    ## 12s
    asvmatrix_in = here('./rawdata/peco/fastq/allyears/20251111_peco-combined_12s_sequence-table_asv-names.txt')
    asv_values = asv_abund(asvmatrix_in)
    # input FASTA
    fasta_in = here('./rawdata/peco/fastq/allyears/20251111_peco-combined_12s_asv-sequences.fasta')
    # output FASTA
    fasta_out = here("./rawdata/peco/fastq/allyears//20251111_peco-combined_12s_sequence-table_swarm-format.fasta")
    # run function to forat to swarm format.
    asv_toswarm(asv_values, fasta_in, fasta_out)


# end
logging.info('Fin!')
