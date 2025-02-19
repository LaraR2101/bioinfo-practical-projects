#!/usr/bin/python3

import urllib.request  # works with ftp server
import argparse
import re
import os


url = 'ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/prokaryotes.txt'
filename = 'GenomeReport.txt'
#check if prokaryotes.txt exists does not exist already
if not os.path.isfile(filename): #only reload file if its not already saved (faster runtime for multiple regEx args)
    urllib.request.urlretrieve(url, filename)
file = open(filename, encoding="utf8")
content = file.read()

parser = argparse.ArgumentParser()
parser.add_argument("--organism", type=str, nargs="+") #list of strings
args = parser.parse_args()

if args.organism:  # if argument was provided
    regex_list = args.organism

else:
    print("Please provide min. one argument for an organism name.")
    exit()


def genome_length(arg, content):

    allList = content.split('\n')  # creates list of strings of file rows

    # filter based on if genome is complete: if row contains "Complete Genome"
    completeGenome = [] #list
    for row in allList:
        if "Complete Genome" in row:
            completeGenome.append(row)

    # create list of dictionaries to store "table"
    dictList = []
    keys = [
        "Organism/Name", "TaxID", "BioProject Accession", "BioProject ID",
        "Group", "SubGroup", "Size (Mb)", "GC%", "Replicons", "WGS",
        "Scaffolds", "Genes", "Proteins", "Release Date", "Modify Date",
        "Status", "Center", "BioSample Accession", "Assembly Accession",
        "Reference", "FTP Path", "Pubmed ID", "Strain"
    ]
    for row in completeGenome:
        columns = row.split('\t')
        dict = {}
        for key, value in zip(keys, columns):
            dict[key] = value

        dictList.append(dict)

    # Filter list of dictionaries based on if input arg is in organism name:
    inputList = []
    for dictionary in dictList:
        if re.search(arg, dictionary["Organism/Name"]) is not None: #Match object of .search is not None if Match
            inputList.append(dictionary.copy())

    # output:
    for dictionary in inputList:
        name = dictionary["Organism/Name"]
        length = dictionary["Size (Mb)"]
        print(name + "\t" + length)


for arg in regex_list:
    genome_length(arg, content)
