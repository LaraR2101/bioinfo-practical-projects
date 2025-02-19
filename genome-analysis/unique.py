#!/usr/bin/python3

import argparse
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()

parser.add_argument("--fasta")
parser.add_argument("--k", nargs="+", type=int)
parser.add_argument("--start", type=int)
parser.add_argument("--p" , help= "gib --p 1 wenn du den plot haben willst sonst lass leer")
parser.add_argument("--ep", help="gib --ep 1 wenn du plot vom E.coli Genom sehen willt")

args = parser.parse_args()

fasta = args.fasta
k_values = args.k
start = args.start
plot = args.p
ecoli_plot = args.ep

def fasta_parser(fasta):
    fasta_dict = {}
    current_id = ""
    current_seq = []
    with open(fasta, "r") as my_file:
        for line in my_file:
            line = line.strip()
            if line.startswith(">"):
                fasta_dict[current_id] = ''.join(current_seq)

                current_id = line[1:]

                current_seq = []

                continue

            current_seq.append(line)

        fasta_dict[current_id] = ''.join(current_seq)
        fasta_dict = {k: v for k, v in fasta_dict.items() if k and v}  # removes empty key&value pairs

        return fasta_dict


def k_mers(fasta_dict, k):
    k_mers_with_ids = {}

    for seq_id, seq in fasta_dict.items():

        seq_length = len(seq)

        if args.start is not None:

             kmer = seq[start:start + k]
             if len(kmer) == k:
                 if kmer not in k_mers_with_ids:
                     k_mers_with_ids[kmer] = set()
                 k_mers_with_ids[kmer].add(seq_id)


        else:
            anzahl = len(seq) - k + 1  # anzahl kmere die generiert werden kann +1 wg 0 index

            for i in range(anzahl):
                kmer = seq[i:i + k]
                if kmer not in k_mers_with_ids:
                    k_mers_with_ids[kmer] = set()
                k_mers_with_ids[kmer].add(seq_id)

    return k_mers_with_ids

def uniq_ids(k_mers_with_ids):
    set_uniq_ids = set()
    for kmer in k_mers_with_ids:
        if len(k_mers_with_ids[kmer]) != 1:
            continue

        set_uniq_ids.update(k_mers_with_ids[kmer])

    return set_uniq_ids


fasta_d = fasta_parser(fasta)
xpoints=[]
ypoints=[]
# for k in k_values:
#   print(k , sep='\t')
for k in k_values:
    dict_kmers = k_mers(fasta_d, k)

    unique_genes_count = len(uniq_ids(dict_kmers))
    percentage_unique = unique_genes_count / len(fasta_d) * 100.0

    xpoints.append(k)
    ypoints.append(percentage_unique)

    length = len(uniq_ids(dict_kmers))


    print(k, length, sep='\t')

# plot for a

if args.p is not None:
    plt.bar(xpoints, ypoints, color='maroon', width=0.3)

    plt.xlabel("K-Werte")
    plt.ylabel("Prozentsatz")
    plt.show()

if args.ep is not None:
    plt.bar(xpoints, ypoints, color='deeppink', width=0.3)
    plt.xlabel("Anzahl der Basen")
    plt.ylabel("Prozentsatz")
    plt.show()


