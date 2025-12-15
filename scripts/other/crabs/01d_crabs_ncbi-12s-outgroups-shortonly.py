#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script queries NCBI using Biopython.
It gets the outgroups for our BLAST database directly using accession numbers

This will extract the fasta for each accession, determine if it is too long, and if it isn't, write it while saving accessions that were too long to assess whether we are missing taxa from this process.

Updated for CRABS 1.0.0

Any license info also goes here
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

LOG_FILENAME = 'ncbi-outgroups-short-log.txt'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
logging.info('Debut!')


# set up functions

# extract our search from the one we set up
def get_search_terms(termsfile):
    with open(termsfile) as f:
        # we just need the first line, technically
        # make it into a list
        first = f.readline()
        data_list = first.split(",")
        #logging.info(f"{data_list}")
        return(data_list)

def fasta_by_acc(query_list, outfile_path, outfile_name, errors):
    # note 'a' if restarting
    with open(here(outfile_path+outfile_name), "a") as out, \
    open(here(outfile_path+errors), "a") as err:
        for q in query_list:
            # each query will search and write to FASTA
            logging.info(q + "is searching")
            handle = Entrez.esearch(
                db='nucleotide', term=q, usehistory="y", retmax="1", idtype="acc")
            search_results = Entrez.read(handle)
            handle.close()
            # use WebEnv
            webenv = search_results["WebEnv"]
            querykey = search_results["QueryKey"]
            acc_list = search_results["IdList"]
            logging.info(acc_list)
            # if we didn't get any ids, don't write
            if not acc_list:
                pass
            else:
                # open handle with search terms
                with Entrez.efetch(
                    db="nucleotide",
                    rettype="fasta",
                    retmode="text",
                    webenv=webenv,
                    query_key=querykey,
                    idtype="acc",
                    ) as fetch_handle:
                    #read the input with SeqIO
                    record = SeqIO.read(fetch_handle, "fasta")
                    # only write sequences less 500,000 base pairs
                    # probably about 1mb? not sure yet
                    if len(record.seq) < 500000:
                        # make one line
                        seq = str(record.seq)
                        # no decimals so its already crabs ready
                        accn_mod = re.sub('\.[1-9]', '\n', record.id)
                        # write to open fasta file
                        out.write(">"+accn_mod+seq+"\n")
                        #SeqIO.write(record, out, "fasta")
                        logging.info(record.id)
                    else:
                        logging.info(record.id + " was too long")
                        seq = str(record.seq)
                        # no decimals so its already crabs ready
                        accn_mod = re.sub('\.[1-9]', '\n', record.id)
                        # write to open fasta file
                        err.write(">"+accn_mod+"\n"+seq)
                        pass




# basic-body

if __name__ == "__main__":

    # set emails
    Entrez.email = "kate.sheridan@mail.mcgill.ca"
    Entrez.api_key = "330c561fca772258d2c869e4caefe8c98b09"
    # Path to fasta output,
    # name of fasta file currently defined in function (change)
    fasta_out_path = ("./database12s/crabs/")
    fasta_new = ("20241006_12s_outgroups-ncbi-filter2.fasta")
    # path to txt for search terms
    # note check if trimmed
    search_terms = (
        "database12s/crabs/20241006_12s_outgroups-ncbi-accn-trim.txt")
    too_long = ('20241006_12s_ncbi-outgroups_toolong.txt')
    # get search terms
    # internet says if "backend failed:" its on NCBI's side
    # so try again later.
    query = get_search_terms(search_terms)
    fasta_by_acc(query, fasta_out_path, fasta_new, too_long)

# end
logging.info('Fin!')
