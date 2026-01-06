#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script queries NCBI using Biopython and fetches taxonomy
Input is a list of accession numbers.
This will

Any license info also goes here
Author: "Kate Sheridan"
Version: "0.1.0"
Status: dev
insert copyright, license, additional credits etc if necessary
"""

# regular expressions
import re
# csv export
import csv
# module import
from Bio import Entrez
# better parser than native Entrez
from Bio import SeqIO
#import xml.etree.ElementTree as ET
from pyprojroot import here  # like here in R

# log-setup
# check logging module for more settings
# I'm mostly using the debug options for development
import logging

LOG_FILENAME = 'ncbi-efetch-taxonomy-log.txt'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
logging.info('Debut!')


# set up functions

def taxonomy_by_acc(query_list, outfile_path, outfile_name):
    # normally w for write but if restarting; a for append
    with open(here(outfile_path+outfile_name), "a") as out, \
    open(here(outfile_path+query_list), "r") as query:
        ncbiwriter = csv.writer(out, delimiter = ",")
        ncbiwriter.writerow(["accession", "organism", "taxonomy"])
        for line in query:
            line = line.strip()
            if line:
            # each query will search and write output
                logging.info(line + "is searching")
                with Entrez.efetch(
                        db="nucleotide",
                        id=line,
                        rettype="gb",
                        retmode="text",
                        idtype="acc",
                        ) as fetch_handle:
                        record = SeqIO.read(fetch_handle, "genbank")
                        logging.info(record.annotations["taxonomy"])
                        ncbiwriter.writerow([record.id, record.annotations["organism"], record.annotations["taxonomy"]])
            else:
                pass

# basic-body

if __name__ == "__main__":

    # set emails
    Entrez.email = "kate.sheridan@mail.mcgill.ca"
    Entrez.api_key = "330c561fca772258d2c869e4caefe8c98b09"
    # Path to fasta output,
    # name of fasta file currently defined in function (change)
    outpath = ("./rawdata/2018calvert/fastq/coi_kate/combined_runs/")
    # path to txt for search terms
    #search_terms = ("20230917_12s_combined-ncbi-accn.txt")
    search_terms = ("20240213_calvert2018_coi_accessions-trim.txt")
    taxonomy_out = ('20240213_calvert2018_coi_taxonomy.csv')
    # get search terms
    taxonomy_by_acc(search_terms, outpath, taxonomy_out)

# end
logging.info('Fin!')
