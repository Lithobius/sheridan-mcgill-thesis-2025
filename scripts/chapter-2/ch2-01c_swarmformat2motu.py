#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Replacing the swarm format with motus
take two
I need to take it from:
>asv#_abundance
actgsequenceactg
to
>motu
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

LOG_FILENAME = 'swarm-unformat-log.txt'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
logging.info('Debut!')


# set up classes and functions
motudic = {}
# read in fasta, sort, write out
def asv2motu(asvkey_in):
    asv_tab = pd.read_csv(asvkey_in)
    # modify to long format; melt
    motudic = asv_tab.set_index(['swarm_reads']).to_dict(orient='dict')['motu']
    logging.info(motudic)
    return(motudic)


def swarm2motu(asv_dict, swarm_fasta, motu_fasta):
    # open old fasta to read and new fasta to write
    with open(swarm_fasta, 'r') as f, \
        open(motu_fasta, 'w') as out:
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
                    out.write(">" + asv_dict[asvnum] + "\n"\
                    +seq+"\n")
                    logging.info('wrote ' + asvnum + " as " + asv_dict[asvnum])
                else:
                    pass
            else:
                pass

# script

if __name__ == "__main__":

    # sequence matrix; columns sequences rows samples values reads
    ## 12s
    asv2motu_key = here('./rawdata/peco/fastq/allyears/swarm/20251111_peco-combined_12s_swarm_statsfile-w-motunums.csv')
    motu_converted = asv2motu(asv2motu_key)
    # input FASTA
    fasta_in = here('./rawdata/peco/fastq/allyears/swarm/20251111_peco-combined_12s_swarm_clusterreps.fasta')
    # output FASTA
    fasta_out = here("./rawdata/peco/fastq/allyears/swarm/20251111_peco-combined_12s_swarm_clusterreps-motus.fasta")
    # run function to forat to swarm format.
    swarm2motu(motu_converted, fasta_in, fasta_out)


# end
logging.info('Fin!')
