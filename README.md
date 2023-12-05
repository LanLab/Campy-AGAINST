# campyagainst
A python script for accurate assignment of ANI genomic species to Campylobacter genomes. 


## Installation

### with conda/mamba - NOT YET AVAILABLE

`conda install -c bioconda campyagainst`

### without conda

`git clone https://github.com/LanLab/campyagainst.git`

`cd campyagainst`

`python setup.py install`

**Note following dependencies must be installed**

* fastANI

## Usage

`campyagainst [-h] -i QUERYFOLDER -o OUTPUTFILE [-t THREADS]`

`-h`, `--help`            show this help message and exit

`-i`,`--query QUERY`    folder containing all input genomes (genomes must have *.fasta suffix)
  
`-o`,`--output`     tabular output file with classifications for each genome in query folder

`-t`, `--thread` number of threads to run fastANI with (default: 4)

## Outputs

A tab delimited file with the following columns:

* **Query Genome** : genome name extracted from file name
* **Highest ANI Value** : The highest ANI value of the query when compared to all centroid genomes
* **Matching centroid genome** : The accession of the highest matching centroid genome
* **ANI cluster number** : The cluster number that the centroid genome represents
* **Campylobacter Genomic Species** : The genomic species name assigned to the matching ANI cluster
* **Possible Novel genomic species** : Whether or not this genome does not match any centroid genome at 94.2% ANI. If True no centroid genomes match indicating that the genome could represent a new species. If True, highest match for other columns is still included but is not reliable.
