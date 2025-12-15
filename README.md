# sheridan-mcgill-thesis-2025
2025 Sheridan Thesis : Applying environmental DNA to track marine biodiversity at continental scales

Code for chapters with intermediate data files.

Begin at scripts > start here 
	under construction 2025-12-12
	need to test renv on second computer


## Chapter 1
Analyses from intermediate files ready
Currently matches PeerJ submitted code

to do; 
	add pipeline
	instructions from ncbi
	update runstats with 12S
	
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

to do;
	add crabs pipeline here as well
	redirect blast from both chapters to the output