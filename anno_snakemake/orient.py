#!/usr/bin/env python3

from operator import attrgetter
import pymummer
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import shutil
import os

#cluster = 'cluster_4'
#ref_fasta = cluster + "/fasta/M10_18.fna"
#qry_fasta = cluster + "/cluster_4.fna"

fastapath = snakemake.params.fastapath
outputpath = snakemake.params.outputpath
genomes = snakemake.params.genomes
ref_fasta = snakemake.params.ref

#nucmer_out = cluster+"/out.nucmer"

# Make a dictionary of query name -> list of matches
qry_to_hits = {}
for match in pymummer.coords_file.reader(snakemake.input.nucmer):
    if match.qry_name not in qry_to_hits:
        qry_to_hits[match.qry_name] = []
    qry_to_hits[match.qry_name].append(match)

# For each query, sort matches by longest to shortest. Use the strand of
# longest to decide whether or not to reverse complement
os.mkdir(f"{outputpath}/oriented_fasta/")
for qry_name, matches in qry_to_hits.items():
    matches.sort(key=attrgetter("hit_length_qry"), reverse=True)
    need_to_revcomp = not matches[0].on_same_strand()
    if need_to_revcomp == True:
        #reverse complement the current genome
        seq_in = SeqIO.read(f"{fastapath}/{qry_name}.fna", "fasta")
        rev = SeqRecord(seq_in.seq.reverse_complement(), qry_name, "", "")
        with open(f"{outputpath}/{oriented_fasta}/{qry_name}.fna", "w") as output_handle:
            SeqIO.write(rev, output_handle, "fasta")
    else:
        shutil.copy(f"{fastapath}/{qry_name}.fna", f"{outputpath}/{oriented_fasta})
remaining = [el for el in genomes if el not in qry_to_hits.keys()]
for el in remaining:
    shutil.copy(f"{fastapath}/{qry_name}.fna", f"{outputpath}/{oriented_fasta}")
