#!/usr/bin/python3

#seclib format: > a FASTA header (id + chain if applicable ?)

# A list of ids must be converted into a seclib-file.
# Most proteins consist of multiple chains. Extract the structure of each chain separately
# (resulting in one sequence per chain) in such cases.
#input: list of ids
#output: file

import requests
from collections import defaultdict
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--id', nargs='+')
args = parser.parse_args()

idList = args.id
# = ["1tim", "1baf"]

# create id.seclib file:
output_path_seclib = 'proteins.seclib'
seclibFile = open(output_path_seclib, 'w')

def printSeclib(id): #for looping through each id in the list
    data = requests.get("https://files.rcsb.org/download/" + id + ".pdb")
    content = data.text

    # Extract lines between first MODEL and ENDMDL if applicable
    start_index = content.find("MODEL")  # Find index of first occurrence
    end_index = content.find("ENDMDL")  # Find index of the first occurrence
    if start_index != -1 and end_index != -1:  # If both model and endmdl exist
        content = content[start_index:end_index]  # Extract only the substring between both

    # turn PDB file into table with columns
    rowsPDB = allList = content.split('\n')  # row for each atom
    filtered_rowsPDB = [line for line in rowsPDB if line.startswith("ATOM")]

    tablePDB = []  # list of dicts for table
    for row in filtered_rowsPDB:
        dictRow = {}  # dictionary for each row
        dictRow['aa'] = row[17:20].strip() #aa type
        dictRow['chain'] = row[21].strip()
        dictRow['residueNumber'] = row[22:26].strip() #aa number
        tablePDB.append(dictRow)

    # Group rows by (residueNumber, chain) tuple
    # defaultdict with lists of grouped rows (key is (residueNumber, chain) and value is matching row from tablePDB)
    grouped_rows = defaultdict(list)
    for row in tablePDB:
        residue_number = row["residueNumber"]
        chains = row["chain"]
        for chain in chains:
            grouped_rows[(residue_number, chain)].append(row)

    # table with combined rows (row for each residueNumber+chain combination)
    tableSscc = []
    for (residue_number, chain), rows in grouped_rows.items():
        row = {}
        for key in rows[0]:  # Just use keys from first row
            row[key] = [r[key] for r in rows]  # Use keys from 1st row to find values in all other rows
        row["residueNumber"] = residue_number
        row["chain"] = chain
        tableSscc.append(row)


    # Assuming combined_table is the list of dictionaries where each dictionary represents a combined row
    for row in tableSscc:
        for key, values in row.items():
            # key != "residueNumber" bc otherwise 11 becomes 1 and 22 becomes 2,... (or turn into int first)
            if key != "residueNumber":  # turn all list values into one value, except residueNumber
                if len(set(values)) == 1:  # if values in list are identical (set allows only unique values)
                    row[key] = values[0]  # if identical simply take first value
                else:
                    print("Not identical values found")
                    print(row[key])



    # ss: sec structure
    # rowsPDB = allList = content.split('\n') # already declared earlier
    filtered_rowsPDB_sec = [line for line in rowsPDB if line.startswith("HELIX") or line.startswith("SHEET")]

    tableSs = []  # list of dicts for table sec struc
    keys = ["residueNumber", "chain", "ss"]

    for row in filtered_rowsPDB_sec:
        columns = row.split()
        if row.startswith("HELIX"):
            start_residue = int(row[21:26].strip())
            end_residue = int(row[33:37].strip())
            chain = row[19:20].strip()
            for residue in range(start_residue, end_residue + 1):
                dictRow = {"residueNumber": residue, "chain": chain, "ss": "H"}  # H is Helix
                tableSs.append(dictRow)
        elif row.startswith("SHEET"):
            start_residue = int(row[22:26].strip())
            end_residue = int(row[34:37].strip())
            chain = row[21:22].strip()
            for residue in range(start_residue, end_residue + 1):
                dictRow = {"residueNumber": residue, "chain": chain, "ss": "E"}  # E is Sheet
                tableSs.append(dictRow)

    # add "ss" to tableSscc:
    # Iterate over tableSscc
    for rowSscc in tableSscc:
        residue_number = int(rowSscc["residueNumber"]) #int bc 'residueNumber': '67' in tableSscc
        chain = rowSscc["chain"]
        match_ss = False

        # Iterate over tableSs to find matching ss entry
        for rowSs in tableSs:
            if (rowSs["residueNumber"], rowSs["chain"]) == (residue_number, chain):
                rowSscc["ss"] = rowSs["ss"]
                match_ss = True
                break #break if match for rowSscc is found

        # If no entry for (aa, chain) in ss table, assign C
        if not match_ss:
            rowSscc["ss"] = "C"  # C for coil if not sheet or helix

    # translate 3 letter amino acids into 1 letter:
    def translate_amino_acid(three_letter_code):
        amino_acids = {
            'ALA': 'A',
            'ARG': 'R',
            'ASN': 'N',
            'ASP': 'D',
            'CYS': 'C',
            'GLN': 'Q',
            'GLU': 'E',
            'GLY': 'G',
            'HIS': 'H',
            'ILE': 'I',
            'LEU': 'L',
            'LYS': 'K',
            'MET': 'M',
            'PHE': 'F',
            'PRO': 'P',
            'SER': 'S',
            'THR': 'T',
            'TRP': 'W',
            'TYR': 'Y',
            'VAL': 'V'
        }
        # Return 1 letter for aa
        return amino_acids.get(three_letter_code)

    for dict in tableSscc:
        dict['aa'] = translate_amino_acid(dict['aa'])

    #seperate sequence for each chain:
    grouped_rows_by_chain = defaultdict(list) #dict: key is each chain and value are rows of that chain
    for row in tableSscc:
        chain = row["chain"]
        grouped_rows_by_chain[chain].append(row)

    for chain, rows in grouped_rows_by_chain.items():
        aa_list = [row['aa'] for row in rows]
        ss_list = [row['ss'] for row in rows]

        seclibFile.write("> " + id + chain +"\n")
        seclibFile.write("AS " + "".join(aa_list) + "\n")
        seclibFile.write("SS " + "".join(ss_list) + "\n")


for id in idList:
    printSeclib(id)