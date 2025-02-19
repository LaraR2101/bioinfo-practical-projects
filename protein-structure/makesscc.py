#!/usr/bin/python3
import requests
from collections import defaultdict
import argparse
import matplotlib

parser = argparse.ArgumentParser()
parser.add_argument('--id', dest='id')
parser.add_argument('--distance', dest='d')
parser.add_argument('--type', dest='t')
parser.add_argument('--length', dest='l')
args = parser.parse_args()

id = args.id
d = args.d
t = args.t
l = args.l
"""
#example input:
#id = "1tim" #PDB file id
id = "1gcn" #very simple example
t = "CA" #Atom Type for contacts
d = 10 #distance for global contacts
l = 3 #distance for local contacts
"""

# PDB file:
data = requests.get("https://files.rcsb.org/download/" + id + ".pdb")
content = data.text

# Sollte die gegebene PDB-Datei mehrere Modelle für ein Protein enthalten, so berechen Sie nur Kontakte fur das erste Modell.
# Extract lines between first MODEL and ENDMDL if applicable
start_index = content.find("MODEL")  # Find index of first occurrence
end_index = content.find("ENDMDL")  # Find index of the first occurrence
if start_index != -1 and end_index != -1:  # If both model and endmdl exist
    content = content[start_index:end_index]  # Extract only the substring between both

# turn PDB file into table with columns
rowsPDB = allList = content.split('\n') #row for each atom
filtered_rowsPDB = [line for line in rowsPDB if line.startswith("ATOM")]

tablePDB_allRows = []  # list of dicts for table
# keys = ["serialNumber", "atomType", "aa", "chain", "residueNumber"]
# !!! serial is number after chain !!!
for row in filtered_rowsPDB:
    dictRow = {}  # dictionary for each row
    dictRow['atomType'] = row[12:16].strip() #CA, CB, ...
    dictRow['serial'] = row[6:11].strip() #atom number /atomID
    dictRow['aa'] = row[17:20].strip() #aa type
    dictRow['chain'] = row[21].strip()
    dictRow['residueNumber'] = row[22:26].strip() #aa number
    dictRow['x'] = float(row[30:38].strip())
    dictRow['y'] = float(row[38:46].strip())
    dictRow['z'] = float(row[46:54].strip())
    tablePDB_allRows.append(dictRow)

# Delete all rows where atom isn't t from tablePDB_allRows
tablePDB = [row for row in tablePDB_allRows if t in row['atomType']]


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


#contacts:

def calculate_distance(row1, row2): #pass 2 rows
    # d = ((x2 - x1)^2 + (y2 - y1)^2 + (z2 - z1)^2)^0.5
    x1, y1, z1 = row1['x'], row1['y'], row1['z']
    x2, y2, z2 = row2['x'], row2['y'], row2['z']
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5
    return distance

def calculate_seqDistance(row1, row2):
    position1 = int(row1["residueNumber"])
    position2 = int(row2["residueNumber"])
    seqDistance = abs(position1 - position2)  # abs makes negative number positive
    return seqDistance

def check_local_global(row1, row2): #pass 2 rows from table
    if calculate_distance(row1, row2) < int(d) and calculate_distance(row1, row2) != 0: #not 0 for same aa
        if row1["chain"] == row2["chain"]: #if same chain
            if calculate_seqDistance(row1, row2) < int(l): #if aa distance < l
                return "local"
            elif calculate_seqDistance(row1, row2) >= int(l): #else if aa distance > l
                return "global"
        elif calculate_seqDistance(row1, row2) >= int(l): #if dif chains
            return "global"

def count_local(row):
    countLocal = 0
    for rows in tableSscc:
        if check_local_global(row, rows) == "local":
            countLocal = countLocal + 1
    return countLocal

def count_global(row):
    countGlobal = 0
    for rows in tableSscc:
        if check_local_global(row, rows) == "global":
            countGlobal = countGlobal + 1
    return countGlobal

for row in tableSscc:
    row["local"] = count_local(row)
    row["global"] = count_global(row)


# ss: sec structure
# ss (careful with chain not just residue position)
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

"""
# add "ss" to tableSscc:
# dictionary to map residueNumbers&chain to ss
residueChain_ss_dict = {(row["residueNumber"], row["chain"]): row["ss"] for row in tableSs}

# update tableSscc with ss information
for rowSscc in tableSscc:
    residue_number = rowSscc["residueNumber"]
    chain = rowSscc["chain"]
    # check if the combination of residue number and chain exists in residueChain_ss_dict
    if (residue_number, chain) in residueChain_ss_dict: #ERROR
        rowSscc["ss"] = residueChain_ss_dict[(residue_number, chain)]
    else:
        # combination chain and residue doesnt exist (i.e. no sec structure info in tableSs)
        rowSscc["ss"] = "C" #C for coil if not sheet or helix
"""

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

#print table for server:
print("chain\tpos\tserial\taa\tss\tglobal\tlocal\n")
for dict in tableSscc:
    print(f"{dict['chain']}\t{dict['residueNumber']}\t{dict['serial']}\t{translate_amino_acid(dict['aa'])}"
                   f"\t{dict['ss']}\t{dict['global']}\t{dict['local']}\n")


# create id.sscc file:
# columns: chain, pos (aa number), serial (atom number), aa, ss, global, local
output_path_sscc = str(id) + '.sscc'
ssccFile = open(output_path_sscc, 'w')
ssccFile.write("chain\tpos\tserial\taa\tss\tglobal\tlocal\n") # header
for dict in tableSscc:
    ssccFile.write(f"{dict['chain']}\t{dict['residueNumber']}\t{dict['serial']}\t{translate_amino_acid(dict['aa'])}"
                   f"\t{dict['ss']}\t{dict['global']}\t{dict['local']}\n")


# contactmatrix C:
# Erzeugen Sie zusätzlich eine Kontaktmatrix C, so dass c(i, j) = 1 genau dann, wenn die
# aa i und j Kontakt haben gemäß der Definition und den Parametern

contact_matrix = []
for row_i in tableSscc:
    matrixRow = []
    for row_j in tableSscc:
        if check_local_global(row_i, row_j) == "local" or check_local_global(row_i, row_j) == "global":
            matrixRow.append(1)
        else:
            matrixRow.append(0)
    contact_matrix.append(matrixRow)

#save contact matrix to file:
file_path_contactM = (str(id) + "_contact_matrix.txt")
with open(file_path_contactM, 'w') as file:
    for row in contact_matrix:
        file.write(str(row) + '\n')



# Erzeugen Sie eine 2d Abbildung, die die Abstände
# im Protein durch Farben visualisiert. Speichern Sie die Abbildung als Datei.
# use heatmap
# create matrix with 3d distances

distance_matrix = []
for row_i in tableSscc:
    matrixRow = []
    for row_j in tableSscc:
        distance = calculate_distance(row_i, row_j)
        matrixRow.append(distance)
    distance_matrix.append(matrixRow)



import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))  # set figure size

#interpolation='nearest': This parameter specifies the interpolation method to be used.
# 'nearest' means that the pixel values are interpolated using the nearest neighbor value.
plt.imshow(distance_matrix, cmap='viridis', interpolation='nearest') #cmap=colormap

plt.colorbar(label='Distance') #colorbar

# labels:
plt.xlabel('Residue Index')
plt.ylabel('Residue Index')
plt.title('Distance Heatmap')

# Save as image file
plt.savefig(str(id) + '_distance_heatmap.png')


