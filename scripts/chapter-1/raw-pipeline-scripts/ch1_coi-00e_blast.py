#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script takes FASTA of ASVs and blasts it to NCBI.
The blast database that Evan is using is just NCBI now, because it includes BOLD.

Any license info also goes here
Author: "Kate Sheridan"
Version: "0.1.0"
Status: dev
insert copyright, license, additional credits etc if necessary
"""

# module import
# built-in
import os

# common libraries
## which of these do I need?
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
#from Bio import Entrez
#from Bio.Blast.Applications import NcbiblastpCommandline
#from Bio import SeqIO
from Bio import SearchIO
from pyprojroot import here  # like here in R

# less-known libraries
# own libraries/functions

# log-setup
# check logging module for more settings
# I'm mostly using the debug options for development
import logging

LOG_FILENAME = 'coi-blast-log.txt'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    format=' %(asctime)s - %(levelname)s - %(message)s')
logging.info('Debut!')


# %% set up general stuff
# fronter to append to all filenames
version = '20240206_'


def reblast(to_blast, blast_out):
    # if fresh
    #with open(to_blast, 'r') as b, \
    #open(blast_out, 'w') as out:
    # if restarting
    with open(to_blast, 'r') as b, \
    open(blast_out, 'a') as out:
        #out.write('<root>\n')
        for line in b:
            # save the sequence
            #seq = next(b)
            if line.startswith('>'):
                seq = next(b)
                asvnum = line[1:-1]
                to_search = ">" + asvnum + "\n" + seq
                logging.info("found " + asvnum)
                blastn_result = NCBIWWW.qblast("blastn",
                                           "nt",
                                           sequence = to_search,
                                           hitlist_size = 50,
                                           perc_ident=90,
                                           megablast=True,
                                           format_type = 'XML'#,
                                           #entrez_query= asvnum,
                                           #results_file=out
                                           )
                results_to_write = blastn_result.read() #append
                out.write(results_to_write)
            else:
                pass
        #out.write('</root>')


def parse_blast(xml_results, tab_out):
    # if fresh
    with open(xml_results, 'r') as b, open(tab_out, 'w') as out:
    # if restarting
    #with open(xml_results, 'r') as b, open(tab_out, 'a') as out:
        out.write("seed_asv_reads" + "\t" + "description" + "\t" + \
        "accession" + "\t" + "identity_percentage" + "\t" + "evalue" +\
        "\t" + "bitscore" + "\n")
        blast_records = NCBIXML.parse(b)
        for record in blast_records:
            logging.info("found: " + record.query)
            if record.alignments == []:
                logging.info("no results")
                out.write(record.query + "\t" + "No Results" + "\n")
            else:
                for alignment in record.alignments:
                    for hsp in alignment.hsps:
                        # looking at the structure to determine what to write
                        #logging.info(dir(alignment))
                        logging.info("wrote: " + alignment.hit_def)
                        perc_id = (hsp.identities / hsp. align_length) * 100
                        out.write(record.query + "\t" + alignment.hit_def + "\t" \
                        + alignment.accession + "\t" + \
                        str(format(perc_id, '.2f')) + "\t" + \
                        str(hsp.expect) + "\t" + str(hsp.score)  + "\n")


if __name__ == "__main__":

    # set emails
    NCBIWWW.email = "kate.sheridan@mail.mcgill.ca"
    # Path to fasta output,
    # name of fasta file currently defined in function (change)
    # fasta_in = here("./rawdata/peco/fastq/allyears/20231023_peco-combined_12s_swarm_problems.fasta")
    # if restarted
    fasta_in = here('./rawdata/2018calvert/fastq/coi_kate/combined_runs/20240213_2018calvert_coi_asv-sequences-noresult.fasta')
    # file to save accession numbers of records that are 'too long' ; whole genomes usually.
    blast_output = ("./rawdata/2018calvert/fastq/coi_kate/combined_runs/20240206_coi-blast_out.xml")
    # get search terms
    #reblast(fasta_in, blast_output)
    # parse results
    blast_parsed = ("./rawdata/2018calvert/fastq/coi_kate/combined_runs/20240206_coi-reblast_out-parsed.tsv")
    parse_blast(blast_output, blast_parsed)

# end
logging.info('Fin!')
