#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The data for 2022 came off the Nextseq with
incorrect names on some of the files. Here we will
correct them before using the normal run processing script.

NOTE: this only needs to be done ONCE,
when the files are downloaded from Hakai servers.

Replacement csv has two columns with headers "sample_id" and "sample_replace".

Author: Kate Sheridan
2024 version 0.1.0
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

LOG_FILENAME = 'rename2023-log.txt'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
logging.info('Debut!')

# set up global variable
name_dic = {}

# set up functions
def new_name(error_files, fixed_files, replace_sheet):
    # open replacesheet to make dictionary
    replace_tab = pd.read_csv(replace_sheet)
    #logging.info(replace_tab)
    name_dic = replace_tab.set_index(['sample_id']).to_dict(orient='dict')['sample_replace']
    #logging.info(name_dic)
    for filename in os.listdir(error_files):
        if filename.endswith('gz'):
            #replace "r'(_)'" with "r'(yourvalue)'"
            bits = re.split(r'(_)', filename)
            #logging.info(bits[1])
            try:
                #replace 0 with intended value (extractions)
                bits[0] = re.sub(bits[0], name_dic[bits[0]], bits[0])
                newname = "".join(bits)
                #logging.info(newname)
            except (KeyError, IndexError):
                try:
                    #replace 4 with intended value (negative pcrs)
                    bits[4] = re.sub(bits[4], name_dic[bits[4]], bits[4])
                    bits[0] = re.sub(bits[0], "PECO2023", "")
                    bits[1] = re.sub(bits[1], "_", "")
                    bits[2] = re.sub(bits[2], "Redos", "")
                    bits[3] = re.sub(bits[3], "_", "")
                    newname = "".join(bits)
                    #logging.info(newname)
                except (KeyError, IndexError):
                    peconum = bits[0] + bits[1] + bits[2]
                    try:
                        bits[0] = re.sub(bits[0], "PECOe", "")
                        bits[1] = re.sub(bits[1], "_", "")
                        bits[2] = re.sub(bits[2], "d+", "")
                        newbits = "".join(bits)
                        peconew = name_dic[peconum]
                        newname = peconew + newbits
                        #logging.info(newname)
                    except (KeyError, IndexError):
                        pass
            #logging.info(newname + " ready!")
            src = str(error_files) + "/" + filename
            fixed = str(fixed_files) + "/" + newname
            logging.info(src + " to " + fixed)
            os.rename(src, fixed)




# script

if __name__ == "__main__":

    ## directory containing "bad" filenames
    direct = here('./rawdata/peco/fastq/12S_PECO2023_Run20240907/Analysis/1/Data/fastq/')
    # destination directory for 'good' files
    dest_direct = here('./rawdata/peco/fastq/12S_PECO2023_Run20240907/Analysis/1/Data/fastq/fixed/')
    ## csv of replacements
    replacements = here('./rawdata/peco/2023_edna/peco_2023_name-replacement.csv')
    # run function to forat to swarm format.
    new_name(direct, dest_direct, replacements)


# end
logging.info('Fin!')
