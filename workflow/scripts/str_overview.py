import sys
import pandas as pd
import logging

logger = logging.getLogger("SimpleLogger")

#sys.stderr = open(snakemake.log[0], "w", buffering=1)
file_handler = logging.FileHandler(snakemake.log[0])
logger.addHandler(file_handler)
logger.setLevel(logging.WARNING)

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
multi = count.index[row_max > 1].tolist()
single = count.index[row_max <= 1].tolist()

# Separate samples with max 1 count per locus for ones with multiple
summary = df.pivot_table(values='count', index=df.index, columns='locus', aggfunc="first")

# Catch samples with no count data
samples_with_data = set(summary.index.to_list())
missing = set(single).difference(samples_with_data)
logger.debug(f"All samples with data: {samples_with_data}")
logger.warning(f"Samples with multiple counts per locus: {multi}")
logger.warning(f"Samples with missing counts: {[*missing]}")
empty_rows = pd.DataFrame(pd.NA, index=[*missing], columns=summary.columns)
for sample in missing:
    single.remove(sample)

single_df = summary.loc[single]
single_df = pd.concat([single_df, empty_rows])
single_df.to_csv(snakemake.output[0], sep="\t", index=True, na_rep='NA')

listed = df.pivot_table(values='count', index=df.index, columns='locus', aggfunc=lambda x: pd.unique(x).tolist())
multi_df = listed.loc[multi]
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
