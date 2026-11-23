# Snakemake workflow: smkwf-STRAf-typing

[![Snakemake](https://img.shields.io/badge/snakemake-≥8.0.0-brightgreen.svg)](https://snakemake.github.io)
[![GitHub actions status](https://github.com/b-brankovics/smkwf-STRAf-typing/actions/workflows/main.yaml/badge.svg?branch=main)](https://github.com/b-brankovics/smkwf-STRAf-typing/actions?query=branch%3Amain+workflow%3ATests)
[![run with conda](http://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/en/latest/)
[![workflow catalog](https://img.shields.io/badge/Snakemake%20workflow%20catalog-darkgreen)](https://snakemake.github.io/snakemake-workflow-catalog/docs/workflows/b-brankovics/smkwf-STRAf-typing)

A Snakemake workflow for STRAf typing Aspergillus fumigatus genome

- [Snakemake workflow: smkwf-STRAf-typing](#snakemake-workflow-smkwf-straf-typing)
  - [Usage](#usage)
  - [Deployment options](#deployment-options)
  - [Workflow profiles](#workflow-profiles)
  - [Authors](#authors)
  - [References](#references)
  - [TODO](#todo)

## Usage

Detailed information about input data and workflow configuration can also be in the [`config/README.md`](config/README.md).

If you use this workflow in a paper, don't forget to give credits to the authors by citing the URL of this repository or its DOI.

## Deployment options

**Prerequisites**:

Snakemake needs to be installed and you need to be able to create conda environments.
You can do this in the following way if you have conda available:

```bash
conda create -n snakemake bioconda::snakemake
conda activate snakemake
```

Download the workflow from github

```bash
git clone git@github.com:b-brankovics/smkwf-STRAf-typing.git
cd smkwf-STRAf-typing
```

**Setup your run**:

Adjust options in the default config file `config/config.yaml` (see [config/README.md](config/README.md)).
Before running the complete workflow, you can perform a dry run using:

```bash
snakemake --dry-run
```

**Running the workflow**:

To run the workflow using **conda**:

```bash
snakemake --cores 8 --sdm conda
```

> The default setting for the workflow is to use conda, use 8 cores and print shell commands (see [profiles/default/config.yaml](profiles/default/config.yaml)).

## Authors

- Balazs Brankovics
  - [Westerdijk Fungal Biodiversity Institute - KNAW](https://wi.knaw.nl/Balazs_Brankovics)
  - [https://orcid.org/0000-0003-0536-7787](https://orcid.org/0000-0003-0536-7787)

