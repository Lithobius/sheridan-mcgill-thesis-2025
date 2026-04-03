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

LOG_FILENAME = 'rename2022-log.txt'

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
                    bits[2] = re.sub(bits[2], name_dic[bits[2]], bits[2])
                    bits[0] = re.sub(bits[0], "PECO2022", "")
                    bits[1] = re.sub(bits[1], "_", "")
                    newname = "".join(bits)
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

    # 2022 run 2 miseq
    ## directory containing "bad" filenames
    direct = here('./rawdata/peco/fastq/miseq_nextseq/miseq_2022_run2/')
    # destination directory for 'good' files
    dest_direct = here('./rawdata/peco/fastq/miseq_nextseq/miseq_2022_run2/fixed/')
    ## csv of replacements
    replacements = here('./rawdata/peco/fastq/miseq_nextseq/peco_2022_name-replacement-run2.csv')
    # run function to forat to swarm format.
    new_name(direct, dest_direct, replacements)

    # 2022 run 2 nextseq
    ## directory containing "bad" filenames
    direct2 = here('./rawdata/peco/fastq/miseq_nextseq/nextseq_2022_run2/')
    # destination directory for 'good' files
    dest_direct2 = here('./rawdata/peco/fastq/miseq_nextseq/nextseq_2022_run2/fixed/')
    # run function to forat to swarm format.
    new_name(direct2, dest_direct2, replacements)


# end
logging.info('Fin!')
