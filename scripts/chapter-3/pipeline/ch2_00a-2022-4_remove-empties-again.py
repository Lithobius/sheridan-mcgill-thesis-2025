#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Some of the FASTQ files are empty.
This moves them to their own folder and writes down which ones.
Note the directory "empty" has to already exist.

Author: Kate Sheridan
2024 version 0.1.0
"""

# load-in
import os
import re
import shutil
from pyprojroot import here # for 'here' like R

# log-setup
# check logging package for more settings
# I'm mostly using the debug options for development
import logging

LOG_FILENAME = 'removeagain2022-log.txt'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
logging.info('Debut!')


# functions

def remove_empties(files_in, files_empty, empties):
    with open(empties, 'w') as f:
        for filename in os.listdir(files_in):
            #extract samplename
            samplename = re.split(r'(_)', filename)[0]
            # make text path for file to extract stats from
            filepath = str(files_in) + "/" + filename
            # get filesize; any fastq.gz less than ~ 50 bytes is empty
            statinfo = os.stat(filepath).st_size
            #logging.info(statinfo)
            if statinfo > 50:
                logging.info(filename + " is ok.")
                pass
            else:
                f.write(samplename + "\n")
                newpath = str(files_empty) + "/" + filename
                shutil.move(filepath, newpath)
                logging.info("Moved empty fastq: " + filename)




# script

if __name__ == "__main__":

    ## directory containing "bad" filenames
    direct = here('./rawdata/peco/fastq/12S_PECO_2022_Redos_Run20250301/Analysis/1/Data/fastq/fixed/filtered')
    # destination directory for 'good' files
    dest_direct = here('./rawdata/peco/fastq/12S_PECO_2022_Redos_Run20250301/Analysis/1/Data/fastq/fixed/empty')
    # list for empties
    empties_list = here('./rawdata/peco/fastq/12S_PECO_2022_Redos_Run20250301/Analysis/1/Data/fastq/fastq_w_no_matches.txt')
    # run function to forat to swarm format.
    remove_empties(direct, dest_direct, empties_list)


# end
logging.info('Fin!')
