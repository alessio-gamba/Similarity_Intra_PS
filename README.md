The datasets reported in the enclosed files have been generated and analyzed, as described in the manuscript "The Similarity of Inherited Diseases (I): Clinical Similarity within the Phenotypic Series" by Gamba A, Salmona M and Bazzoni G (BMC Medical Genomics, 2020, submitted)

Outputs folder:

File 'd_dp.txt' is the D-DP, with 5,818 N (2,118 as D; 3,700 as DP) and 26,539 E (as D-DP pairs). It is taken from table 'bipartite' in module 3 of the SQL script. The columns are mim_id (the Disease, D, in the phen_mim identifier from OMIM), hpo_id (the Disease Phenotype, DP, in the hp identifier from HPO) and ic (the information content, IC, of the DP).

File 'ddsn_c.txt' is the complete DDSN-C with 2,116 N (D as OMIM identifers) and 624,610 E (as Di-Dj pairs). It is taken from table tmp6_ddsn of module 6.3 in the SQL script. The columns are mim_id_i (the first D or Di), ic_mean (the average of the IC of the shared DP) and mim_id_j (the second D or Dj).

Python code:

The first script is 'Sim_calculator.py' (running under Python 2).
It generates a very big file (58 MB) with similarities calculated between all possible pairs of OMIM Diseases.
Similarities are calculated based on HPO annotation of diseases.
The file with similarities is necessary to proceed in the analysis.

The second script is 'Analysis_of_similarity.py' (running under Python 2).
It generates two files: 'Sim_mean.txt' and 'Sim_max.txt' (now in the outputs folder)

The scripts cannot work without 3 input files (not provided here but available):
1. hp.obo
2. OMIM_ALL_FREQUENCIES_diseases_to_genes_to_phenotypes.txt
3. PhenSer.txt

The first two are, respectively, the HP ontology and the list of diseases with their terms of annotation. They can be downloaded from the HPO web site.
The last file contain information on how OMIM diseases are grouped in Phenotypic Series. It is available from OMIM team upon request.
