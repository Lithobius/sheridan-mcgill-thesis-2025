#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script queries NCBI using Biopython.

Here we will use a search query and download a fasta of results below 500,000 base pairs into a FASTA, with accession numbers indicating that it was above that into a text file to be queried later.

Updated for Crabs 1.0.0 release

Author: "Kate Sheridan"
Version: "0.2.0"
Status: dev
insert copyright, license, additional credits etc if necessary
"""

# regular expressions
import re
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

LOG_FILENAME = 'ncbi-fish-short-log.txt'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
logging.info('Debut!')


# set up functions
def fasta_by_search(query_list, outfile_path, outfile_name, errors):
    with open(here(outfile_path+outfile_name), "w") as out, \
    open(here(outfile_path+errors), "w") as err:
    # search enterez for records that match the query
        handle = Entrez.esearch(
            db='nucleotide', term=query_list, usehistory="y", \
            idtype="acc")
        search_results = Entrez.read(handle)
        handle.close()
        # use WebEnv
        webenv = search_results["WebEnv"]
        querykey = search_results["QueryKey"]
        acc_list = search_results["IdList"]
        # for troubleshooting
        #count = 50
        count = int(search_results["Count"])
        logging.info("Records found: "+str(count))
        # How many records at once?
        batch_size = 200
        for start in range(0, count, batch_size):
            end = min(count, start + batch_size)
        # each query will search and write to FASTA
            logging.info("Searching for... "+str(start)+" to "+str(end))
            # open handle with search terms
            fetch_handle = Entrez.efetch(db="nucleotide", \
                rettype="fasta", \
                retmode="text", \
                retstart=start, \
                retmax=batch_size, \
                webenv=webenv, \
                query_key=querykey, \
                idtype="acc")
                #read the input with SeqIO
            for record in SeqIO.parse(fetch_handle, "fasta"):
                # only write sequences less 500,000 base pairs
                # probably about 1mb? not sure yet
                if len(record.seq) < 500000:
                    # make one line
                    seq = str(record.seq)
                    # no decimals so its already crabs ready
                    accn_mod = re.sub('\.[1-9]', '\n', record.id)
                    # write to open fasta file
                    out.write(">"+accn_mod+seq+"\n")
                    logging.info(record.id)
                else:
                    logging.info(record.id + " was too long")
                    # no decimals so its already crabs ready
                    accn_mod = re.sub('\.[1-9]', '\n', record.id)
                    # write to open fasta file
                    err.write(accn_mod)




# basic-body

if __name__ == "__main__":

    # set emails
    Entrez.email = "kate.sheridan@mail.mcgill.ca"
    Entrez.api_key = "330c561fca772258d2c869e4caefe8c98b09"
    # Path to fasta output,
    # name of fasta file currently defined in function (change)
    fasta_out_path = ("./database12s/crabs/")
    fasta_new = ("20241010_12s_fish-ncbi-filter.fasta")
    # search for ncbi
    query = "((((((Myxini[Organism]) OR Actinopterygii[Organism]) OR Dipnomorpha[Organism]) OR Chondrichthyes[Organism]) OR Hyperoartia[Organism]) OR Coelacanthimorpha[Organism]) AND 12S"
    # file to save accession numbers of records that are 'too long' ; whole genomes usually.
    too_long = ('20241010_12s_ncbi-fish_toolong.txt')
    # get search terms
    fasta_by_search(query, fasta_out_path, fasta_new, too_long)

# end
logging.info('Fin!')
