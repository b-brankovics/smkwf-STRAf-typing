import sys
import pandas as pd

sys.stderr = open(snakemake.log[0], "w", buffering=1)

# input files
str_file = snakemake.input["STR"]
results_file = snakemake.input["tsv"]

# sample name
sample = snakemake.wildcards["sample"]

# load tables
str_df = pd.read_csv(str_file, sep="\t")
res_df = pd.read_csv(results_file, sep="\t")

# keep only STRAf loci
res_df = res_df[res_df["test"].str.startswith("STRAf")]
# filter out unrealistic sized amplicons
res_df = res_df[res_df["amplicon size"] < 1000]

# Process each locus
with open(snakemake.output[0], mode="w") as out:
    out.write("\t".join(["sample", "locus", "count"+ "\n"]))
    for index, row in str_df.iterrows():
        # Get PCR test values for the locus to calculate or print NA
        select = res_df.loc[res_df['test'] == row["locus"]]
        if select.shape[0]:
            for index, res_row in select.iterrows():
                out.write("\t".join([sample, row["locus"], str((res_row["amplicon size"] - row["flanking_len"]) / row["repeat_len"]) + "\n"]))
        else:
            out.write("\t".join([sample, row["locus"], "NA\n"]))
