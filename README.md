# sheridan-mcgill-thesis-2025
2025 Sheridan Thesis : Applying environmental DNA to track marine biodiversity at continental scales

Code for chapters with intermediate data files.

Begin at scripts > start here 
	under construction 2025-12-15
	need to test renv on second computer
	need to set up pyenv


## Chapter 1
Analyses from intermediate files ready
Currently matches PeerJ submitted code

to do; 
	add pipeline
	add space to build blast database
	instructions from ncbi
	update runstats with 12S
	
	
scripts
	calvert_map
		rmarkdown
		map of calvert island and sampling locations
	calvert-runstats
		tracks reads throughout qc
	12s-00_regional-species-pool
		rmarkdown
		makes regional species pool for fish
	12s-02_compare-species
		rmarkdown
		compares venn diagrams of regional species pool, blast database, and eDNA results
	12s-03a_inext-compare
		rmarkdown
		compares iNEXT of different subsets
	12s-03b_inext-readnumber
		rmarkdown
		simulates read numbers and makes relevant iNEXT plots
	coi-02_compare species
	coi-03a_inext-compare
		same as 12s but coi
	coi-03b_inext-readnumber
		same as 12s but coi
	

## Chapter 2

Analyses from intermediate files ready

Note the OBIS-GBIF files and raw spatial files must be generated from scratch as the intermediate files are too large for github.

to do;
	add pipeline
	obis-gbif test
	add thermal affinity download scripts 
	test thermal affinity download scripts
	
scripts
	01_ednaprocessing
		R markdown, contains pipeline (needs updated for all years)
		Note in the current form there are steps where you have to run the corresponding python script before continuing.
	01b_seqtable2swarm.py
		python; needs run before SWARM.
		reformats sequence table to proper format
	01c_swarmformat2motu.py
		python; needs run after SWARM.
		updates SWARM output to an MOTU table
	01d_remove-motus-from-fasta.py
		python; run after LULU to remove clusters that were curated into existing clusters
	02_blast
		rmarkdown, requires BLAST database (in process)
		blasts all ASVs for top 50, reannotates ncbi accessions with keys, and performs taxonomic assignment.
	03_byyearqc
		rmarkdown
		adds taxonomy and metadata to samples by year. notes species found in negative controls and indicates which ones would go to 0 with read subtraction if this QC is needed. Also runs whole dataset through DESeq2 to control batch effects.
	04_bubbleplot
		rmarkdown
		takes the qc'd data and generates bubble plots that go into figure 1
	05_getobisgbif
		rmarkdown
		fetches obis and gbif data, cleans, and combines into one dataset
			2025-12-12 script is currently untested after pasting from original chapter 2 repository
	05b_subset-to-sites
		rmarkdown
		takes obis and gbif data, matches records to region by latitude, then to site with geosphere.
	06_get-environment
		rmarkdown
		uses rerddap to get sea surface temperature data from the dataset: NOAA ERD and CoastWatch West Coast Regional Node,Multi-scale Ultra-high Resolution (MUR) SST Analysis fv04.1, Global, 0.01°, 2002-present Monthly	
		then calculates seasonal values, makes a raster, and assigns summary statistics to PECO sites
		also downloads BEUTI upwelling
	07_pcoa
		rmarkdown
		PCoA for OBIS/GBIF subsets and eDNA data; all years and all years together
	08a_thermal-affinity-extract-obis
		rmarkdown
		extracts all occurrences of species in the eDNA data from obis
	08b_thermal-affinity-extract-pathfinder
		rmarkdown
		extracts sea surface temperature for OBIS records using bounding boxes around the obis points
	09a_thermal-affinity
		rmarkdown
		calculates thermal affinity statistics
	09b_thermal-affinity-models
		rmarkdown
		runs the mixed effect linear models for thermal affinity
	10_range-comparison
		rmarkdown
		compares latitudinal ranges of literature, obis-gbif, and eDNA
	11_misc-stats
		rmarkdown
		calculates stats for tables; read counts
	mapping
		rmarkdown
		makes maps of study area and partners
		
			
## other

Includes nextseq control analysis

CRABS
### Reference Database Instructions

The latest version was generated from a CRABS database from my chapter 1 repository.
Right now there are a few possible methods in the folder for extracting NCBI info.
UPDATE to most recent version
note this might make slightly different assignments than thesis because the database is too large for github
To access the database used, created on 2024-10-21: https://zenodo.org/records/17943978 ; doi 10.5281/zenodo.17943977
Place this into the following directory: ./processeddata/blastdb/blastdb_202410


First, we need to run CRABS from the CRABS folder to generate the initial database.
todo; test and update these; find the description from the other readme (gapp folder?)
	`00` scripts are to process initial downloads/etc.
	`extract-taxonomy` would be from a NCBI summary file
	`extract-taxonomy_tinyseq` would be from an NCBI tinyseq file
	`extract_ncbinum` is from the crabs database FASTA
	`01_fish_ncbi-efetch-taxonomy.py` takes the output from `extract-ncbinum` or any txt file that's a list of ncbi numbers to query ncbi for taxonomy using efetch. Currently it does not have a method to handle problems from NCBI and will sometimes throw an error and stop the loop. But there is nothing wrong with the record, it just needs to be restarted.
	`01a_trimlist.py` will trim the list of accession numbers for when efetch-taxonomy hangs up and stops. This way the script can be easily restarted and won't have to rewrite numbers
	`02_fish_ncbi2worms.Rmd` Goes through the output from efetch taxonomy to: indicate gene(s) from accession number, generate a verbatim name to match, match with worms

to do;
	redirect blast from both chapters to the directory