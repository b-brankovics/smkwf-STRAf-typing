import sys
import pandas as pd

sys.stderr = open(snakemake.log[0], "w", buffering=1)

# input files
# str_file = snakemake.input["STR"]
results_files = snakemake.input["counts"]

# # sample name
# sample = snakemake.wildcards["sample"]

# load tables
df = pd.concat((pd.read_csv(f, sep="\t") for f in results_files), ignore_index=True)
df.set_index("sample", inplace=True)
# str_df = pd.read_csv(str_file, sep="\t")

# list multiple options
# summary = df.pivot_table(values='count', index=df.index, columns='locus', aggfunc=lambda x: pd.unique(x).tolist())

# Check the number of repeat counts per locus and sample
count = df.pivot_table(values='count', index=df.index, columns='locus', aggfunc="count")
# row-wise max
row_max = count.max(axis=1)
multi = count.index[row_max > 1]
single = count.index[row_max <= 1]

# Separate samples with max 1 count per locus for ones with multiple
summary = df.pivot_table(values='count', index=df.index, columns='locus', aggfunc="first")

single_df = summary.loc[single.tolist()]
single_df.to_csv(snakemake.output[0], sep="\t", index=True, na_rep='NA')

listed = df.pivot_table(values='count', index=df.index, columns='locus', aggfunc=lambda x: pd.unique(x).tolist())
multi_df = listed.loc[multi.tolist()]
multi_df.to_csv(snakemake.output[1], sep="\t", index=True, na_rep='NA')

# with open(snakemake.output[0], mode="w") as out:
#     out.write("\t".join(["sample", "locus", "count"+ "\n"]))
#     for index, row in str_df.iterrows():
#         # Get PCR test values for the locus to calculate or print NA
#         select = res_df.loc[res_df['test'] == row["locus"]]
#         if select.shape[0]:
#             for index, res_row in select.iterrows():
#                 out.write("\t".join([sample, row["locus"], str((res_row["amplicon size"] - row["flanking_len"]) / row["repeat_len"]) + "\n"]))
#         else:
#             out.write("\t".join([sample, row["locus"], "NA\n"]))
