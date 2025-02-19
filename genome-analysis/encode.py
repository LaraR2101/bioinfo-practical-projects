#!/usr/bin/python3

import argparse
import copy
from collections import Counter
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='input_path')
parser.add_argument('--output', dest='output_dir')
args = parser.parse_args()

input_path = args.input_path
output_dir = args.output_dir

with open(input_path) as file:
    content = file.readlines()
header = content[0].strip().split(',')  # creates list of strings of column headers
rows = content[1:]

# Create list of dictionaries to store CSV table
listDict = []
for row in rows:
    row_values = row.strip().split(',')
    dictRow = {} #dict to store each row in
    #if the number of columns in the row matches the number of columns in the header
    if len(row_values) == len(header):
        for i, value in enumerate(row_values):
            dictRow[header[i].strip()] = value.strip()
    else: #error in csv file: if more columns in row than header then merge the split col 3 in col 3 and 4
        merged_values = row_values[:2] + [row_values[2] + ' ' + row_values[3]] + row_values[4:]
        for i, value in enumerate(merged_values):
            dictRow[header[i].strip()] = value.strip()
    # Append the row dictionary to the list of dictionaries
    listDict.append(dictRow)


    #PART 1:

data_types = [row['Data_Type'] for row in listDict] #extract all data types
data_type_counts = Counter(data_types) #use collections Counter to count the occurences of each type

output_file = output_dir + '/exptypes.tsv'

# Save to .tsv file
tsvFile = open(output_file, 'w', newline='')
for data_type, count in data_type_counts.items():
    tsvFile.write(data_type + "\t" + str(count) + "\n")


    #PART 2
#antibodies.tsv:
#Count die Anzahl verschiedener ChIP-seq Antikorper fur jede Zelllinie
#(auch Zelllinien ohne ChIP-seq Experimente) und gib eine entsprechende Tabelle aus.

cellLine_antibodies_unique = defaultdict(set) #default dict of sets, no duplicate values possible so only unqiue antibodies

# Iterate through listDict and collect unique antibodies for each Cell_Type
for row in listDict:
    cell_type = row['Cell_Type']
    experimental_factors = row['Experimental_Factors'] #column with antibody info
    if row['Data_Type'] != "ChIP-seq":
        antibodies = set() #if not a ChIP-Seq then antibody should not get counted so empty set
    else:
        antibodies = [factor.split('=')[1].strip() for factor in experimental_factors.split() if
                      factor.startswith('Antibody=')]
    cellLine_antibodies_unique[cell_type].update(antibodies)


# dict to store the count (len()) of unique antibodies for each Cell_Type
cell_antibodies_counts = {cell_type: len(antibodies) for cell_type, antibodies in cellLine_antibodies_unique.items()}

# .tsv file
output_file_antibodies = output_dir + '/antibodies.tsv' #path
antibodyFile = open(output_file_antibodies, 'w', newline='')
for cell_type, count in cell_antibodies_counts.items():
    #debug=sorted(cellLine_antibodies_unique[cell_type])
    antibodyFile.write(f"{cell_type}\t{count}\n")



    # PART 3

# new table with added column with antibody used to each row (None if no antibodies)
# Clone the listDict
listDict_antibodies = copy.deepcopy(listDict) #deepcopy bc no change to og copy

for row in listDict_antibodies:
    experimental_factors = row['Experimental_Factors']
    # Split Experimental_Factors first by whitespace then by = and extract the antibody
    antibodies = [factor.split('=')[1].strip() for factor in experimental_factors.split() if factor.startswith('Antibody=')]

    # Add the 'antibody' key to the row dictionary with the extracted antibody value
    if antibodies:
        row['antibody'] = antibodies[0]  # [0] assigns first value bc there is max one antibody anyway
    else:
        row['antibody'] = None  # if no antibody is found


#create sets of cell types that fullfill conditions of data type chip or rna (and sepcified antibody for chip)

# Find cell types with ChIP-seq and antibody H3K27me3
chip_h3k27me3_cell_types = {row["Cell_Type"] for row in listDict_antibodies
                            if row.get("Data_Type") == "ChIP-seq" and row.get("antibody") == "H3K27me3"}


# Find cell types with RNA-seq
rna_seq_cell_types = {row["Cell_Type"] for row in listDict_antibodies
                      if row.get("Data_Type") == "RNA-seq"}

# Find common cell types aka intersection
common_cell_types = chip_h3k27me3_cell_types.intersection(rna_seq_cell_types)


# dict only rows with cell types with ChIp and RNA-Seq (common_cell_types)
listDict_Chip_RNA = [row for row in listDict_antibodies
                  if row.get("Cell_Type") in common_cell_types]


# defaultdict to store accession values for each cell line that fulfill conditions H3K27me3 and ChIP/RNA
cell_line_data = defaultdict(lambda: {"RNAseq Accession": [], "ChIPseq Accession": []})

#find accession numbers of all cell types that fullfill the conditions
for row in listDict_Chip_RNA:
    cell_line = row["Cell_Type"]
    accession = row["DCC_Accession"]
    data_type = row["Data_Type"]
    antibody = row.get("antibody")

    if data_type == "RNA-seq":
        cell_line_data[cell_line]["RNAseq Accession"].append(accession)
    elif data_type == "ChIP-seq" and antibody == "H3K27me3":
        cell_line_data[cell_line]["ChIPseq Accession"].append(accession)


# .tsv file
output_file_seq = output_dir + '/chip_rna_seq.tsv'
with open(output_file_seq, "w") as f:
    # columns header
    f.write("cell line\tRNAseq Accession\tChIPseq Accession\n")

    # rows
    for cell_line, accessions in cell_line_data.items():
        # Filtering out empty DDC fields (with if a) and sorting ascending (with sorted)
        rna_accession = ",".join(sorted(a for a in accessions["RNAseq Accession"] if a))
        chip_accession = ",".join(sorted(a for a in accessions["ChIPseq Accession"] if a))

        f.write(f"{cell_line}\t{rna_accession}\t{chip_accession}\n")

