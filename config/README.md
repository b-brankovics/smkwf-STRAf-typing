## Workflow overview

This workflow extracts PCR amplicon regions from genomes, and then can process them for STR typing.
The workflow is built using [snakemake](https://snakemake.readthedocs.io/en/stable/) and consists of the following steps:

> Need to update

## Running the workflow

### Input data

This workflow extracts PCR amplicon regions from genomes, and then can process them for STR typing.
You need to specify four tables (TSVs) and a yaml file (primers.yaml) as inputs:

accessions.tsv:

| sample    | assembly        |
| --------- | --------------- |
| Af293	    | GCF_000002655.1 |
| A1160     | GCA_024220425.1 |
| W72310    | GCA_040167795.1 |
| ATCC46645 | GCA_040142955.1 |

local.tsv:

| sample    | assembly_file                      |
| --------- | ---------------------------------- |
| sample1   | data/genomes/sample1_contigs.fasta |
| sample2   | data/genomes/sample2_contigs.fasta |
| sample3   | data/genomes/sample3_contigs.fasta |

STR.tsv:

| locus    | flanking_len | repeat_len | repeat_seq |
| -------- | ------------ | ---------- | -----------|
| STRAf-2A | 143          | 2          | GA         |
| STRAf-2B | 107          | 2          | AG         |
| STRAf-2C | 139          | 2          | CA         |
| STRAf-3A | 106          | 3          | TCT        |
| STRAf-3B | 134          | 3          | AAG        |
| STRAf-3C | 62           | 3          | TAG        |
| STRAf-4A | 145          | 4          | TTCT       |
| STRAf-4B | 145          | 4          | CTAT       |
| STRAf-4C | 141          | 4          | ATGT       |

primers.tsv:

| Locus    | Description             | Name      | Sequence              | OligoType | Reference                           |
| -------- | ----------------------- | --------- | --------------------- | --------- | ----------------------------------- |
| STRAf-2A | Microsatellite locus 2A | STRAf-2AF | AAGGGTTATGGCCATTAGGG  | F         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-2A | Microsatellite locus 2A | STRAf-2AR | GACCTCCAGGCAAAATGAGA  | R         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-2B | Microsatellite locus 2B | STRAf-2BF | TATTGGATCTGCTCCCAAGC  | F         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-2B | Microsatellite locus 2B | STRAf-2BR | GAGATCATGCCCAAGGATGT  | R         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-2C | Microsatellite locus 2C | STRAf-2CF | TCGGAGTAGTTGCAGGAAGG  | F         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-2C | Microsatellite locus 2C | STRAf-2CR | AACGCGTCCTAGAATGTTGC  | R         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-3A | Microsatellite locus 3A | STRAf-3AF | GCTTCGTAGAGCGGAATCAC  | F         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-3A | Microsatellite locus 3A | STRAf-3AR | GTACCGCTGCAAAGGACAGT  | R         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-3B | Microsatellite locus 3B | STRAf-3BF | CAACTTGGTGTCAGCGAAGA  | F         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-3B | Microsatellite locus 3B | STRAf-3BR | GAGGTACCACAACACAGCACA | R         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-3C | Microsatellite locus 3C | STRAf-3CF | GGTTACATGGCTTGGAGCAT  | F         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-3C | Microsatellite locus 3C | STRAf-3CR | GTACACAAAGGGTGGGATGG  | R         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-4A | Microsatellite locus 4A | STRAf-4AF | TTGTTGGCCGCTTTTACTTC  | F         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-4A | Microsatellite locus 4A | STRAf-4AR | GACCCAGCGCCTATAAATCA  | R         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-4B | Microsatellite locus 4B | STRAf-4BF | CGTAGTGACCTGAGCCTTCA  | F         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-4B | Microsatellite locus 4B | STRAf-4BR | GGAAGGCTGTACCGTCAATCT | R         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-4C | Microsatellite locus 4C | STRAf-4CF | CATATTGGGAAACCCACTCG  | F         | DOI:10.1128/jcm.43.8.4112-4120.2005 |
| STRAf-4C | Microsatellite locus 4C | STRAf-4CR | ACCAACCCATCCAATTCGTAA | R         | DOI:10.1128/jcm.43.8.4112-4120.2005 |


### Parameters

This table lists all parameters that can be used to run the workflow.

| parameter             | type | details                                             | default                 |
| --------------------- | ---- | --------------------------------------------------- | ----------------------- |
| **accessions**        | path | path to sample sheet of accessions, mandatory       | "config/accessions.tsv" |
| **local_samples**     | path | path to sample sheet of local assemblies, mandatory | "config/local.tsv"      |