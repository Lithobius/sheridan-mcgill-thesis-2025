#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
To resolve the issue with improperly paired files, the fastqCombinePairedEnd.py script works by matching the names and removing any orphan reads. This way the reads are lined up as expected by cutadapt.

However that is a script that works on one file at a time, so we will write a loop to run it on everything, then sort the files afterwards so that the original processing script can be used on the newly paired files.

Any license info also goes here
Author: "Kate Sheridan"
Version: "0.1.0"
Status: dev
insert copyright, license, additional credits etc if necessary
"""

# module import
# built-in
import os
import runpy
import sys
import shutil

# common libraries
from pyprojroot import here # like here in R

# less-known libraries
# own libraries/functions

# log-setup
# check logging module for more settings
# I'm mostly using the debug options for development
import logging

LOG_FILENAME = 'repairfastqloop2022-log.txt'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
logging.info('Debut!')

# global
file2sampleFW = {}
file2sampleR = {}
datefield = '20240923_'

# set up functions
# First we want to pair the files with fastqCombinePairedEnd
def pairfastqs(targetDirectory):
    for file in os.listdir(targetDirectory):
        if file.endswith('R1_001.fastq.gz'):
            samplename = file.split("_")[0]
            #logging.info(samplename)
            # dictionary of sample names
            file2sampleFW[file] = [samplename]
        elif file.endswith('R2_001.fastq.gz'):
            samplename = file.split("_")[0]
            #logging.info(samplename)
            # dictionary of sample names
            file2sampleR[samplename] = [file]
        else:
            pass
    logging.info(file2sampleR)
    logging.info(file2sampleFW)

def runPairScript(targetDirectory, targetScript):
    for key in file2sampleFW:
        logging.info(key)
        # get value and replace the dictionary bits
        samplename = str(file2sampleFW.get(key, 0)).replace("[", "").replace("]", "").replace("'","")
        logging.info(samplename)
        # get R filename from matching samplename
        file2 = str(file2sampleR.get(samplename)).replace("[", "").replace("]", "").replace("'","")
        logging.info('paired ' + file2)
        #now run the script!!!!
        runpy.run_path(targetScript, init_globals={
        'in1': str(targetDirectory)+'/'+key,
        'in2': str(targetDirectory)+'/'+file2,
        'separator': " "
        }, run_name='__main__')

# then we want to move the improperly paired and singleton files to a new directory
def sortPairs(targetDirectory, targetSingles, targetOriginal):
    for file in os.listdir(targetDirectory):
        if file.endswith('_pairs_R1_001.fastq.gz'):
            pass
        elif file.endswith('_pairs_R2_001.fastq.gz'):
            pass
        elif file.endswith('_singles.fastq.gz'):
            logging.info(file + ' singles')
            shutil.move(os.path.join(targetDirectory, file), targetSingles)
        elif file.endswith('_R1_001.fastq.gz'):
            shutil.move(os.path.join(targetDirectory, file), targetOriginal)
            logging.info(file + ' original R1, done')
        elif file.endswith('_R2_001.fastq.gz'):
            logging.info(file + ' original R2')
            shutil.move(os.path.join(targetDirectory, file), targetOriginal)
        else:
            pass

# then we want to remove the added characters from the script
def renamePairs(targetDirectory, targetOriginal):
    for file in os.listdir(targetDirectory):
        if file.endswith('_pairs_R1.fastq.gz'):
            filename = datefield + file.replace('_pairs_R1.fastq.gz', '')
            logging.info(file)
            os.rename(os.path.join(targetDirectory,file), os.path.join(targetDirectory,filename))
        elif file.endswith('_pairs_R2.fastq.gz'):
            logging.info(file)
            filename = datefield + file.replace('_pairs_R2.fastq.gz', '')
            os.rename(os.path.join(targetDirectory,file), os.path.join(targetDirectory,filename))
        else:
            pass
    for file in os.listdir(targetOriginal):
        if file.endswith('.fastq.gz'):
            logging.info(file)
            filename = "original_"+file
            os.rename(os.path.join(targetOriginal,file), os.path.join(targetOriginal,filename))
        else:
            pass


# basic-body

if __name__ == "__main__":

    # Pairing script to make the fastq files happy
    pairscript = here("./scripts/fastqCombinePairedEnd.py")

    # September run of PECO 2023
    fastqDirectory = here("./rawdata/peco/fastq/12S_PECO_2022_Redos_Run20250301/Analysis/1/Data/fastq/fixed")
    singlesDirectory = here("./rawdata/peco/fastq/12S_PECO_2022_Redos_Run20250301/Analysis/1/Data/fastq/fixed/singles/")
    originalsDirectory = here("./rawdata/peco/fastq/12S_PECO_2022_Redos_Run20250301/Analysis/1/Data/fastq/fixed/improperlypaired/")

    #
    pairfastqs(fastqDirectory)
    runPairScript(fastqDirectory, pairscript)
    sortPairs(fastqDirectory, singlesDirectory, originalsDirectory)
    renamePairs(fastqDirectory, originalsDirectory)




# write code here
# don't forget logging.debug('message' or object) periodically


# end
logging.info('Fin!')
