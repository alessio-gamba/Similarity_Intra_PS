## The Similarity intra Phenotypic Series

The datasets reported in the enclosed files have been generated and analyzed, as described in the manuscript entitled ‘The Similarity of Inherited Diseases (I): Clinical Similarity Within the Phenotypic Series’ by Gamba A, Salmona M and Bazzoni G (Submitted to BMC Medical Genomics, Revised December 4, 2020)

### A. SQL folder

A.1 The file similarity_intra_ps_sql.docx contains

(i) the I/O diagram and

(ii) the scripts performed in SQL (with SQLite 3.23.1).

It is subdivided into six modules, as described hereafter (1.1 to 1.6).

  A.1.1. The OMIM-derived genetic diseases (D) and their grouping into the Phenotypic Series (PS)
  
  A.1.2. The Human Phenotype Ontology (HPO)-derived Disease Phenotypes (DP) annotating the OMIM-derived D
  
  A.1.3. The preliminary D-DP bipartite graph simply obtained by linking a D (from module 1) with a DP (from module 2)
  
  A.1.4. The pairing of all the DP and the dentification of the shared DP ancestor(s).
  
  A.1.5. The etiological annotations of the D (according to Disease Ontology; DO) mapped onto the D and the PS.
  
  A.1.6. The definitive bipartite D_DP and the DDSN_C network.


A.2 The following outputs generated in SQL

  A.2.1 File 'd_dp.txt' is the D-DP, with 5,818 N (2,116 as D; 3,107 as DP) and 51,657 E (as D-DP pairs). It is derived from table 'd_dp' in module A.1.6 of the SQL script.
  The  columns are mim_id (Disease, D, in the mim_id identifier from OMIM), hpo_id (Disease Phenotype, DP, in the hp identifier from HPO) and
  ic (information content, IC, of the DP).
  
  A.2.2 File 'ddsn_c.txt' is the complete DDSN-C with 2,116 N (D as OMIM identifers) and 624,610 E (as Di-Dj pairs). It is derived from table ddsn of module A.1.6.3 of SQL.
  The columns are mim_id_i (the first D or Di), ic_mean (the average of the IC of the shared DP) and mim_id_j (the second D or Dj).




### B. Python folder

The two scripts, "Sim_calc.py" and "Analysis_of_similarity.py", are written for Python 3 (or Python 2 with few minor changes).
All the generated outputs are also provided in the Python folder.


INPUTS for the two scripts

1. "hp.obo". This file is the Human Phenotype Ontology (HPO) in obo format. It is not provided here because it is freely available at HPO site (https://hpo.jax.org/app/).
2. "OMIM_ALL_FREQUENCIES_diseases_to_genes_to_phenotypes.txt". This file provides OMIM diseases with their terms of annotations (one or more terms for each disease). It is not provided here because it is freely available as HPO.
3. "PhenSer.txt". This file enlists OMIM Phenotypic Series (PS) with their associated diseases (with MIM code). This information is available on the OMIM site (www.omim.org) and the complete list of PS can be obtained upon request to OMIM team. For this reason the file is not provided here.


OUTPUTS of the two scripts

The first script to run is "Sim_calc.py", it requires the 3 input files mentioned above. This program calculates similarities of all possible pairs of diseases present in PS, based on the annotation terms of the diseases. It also calculates and returns the Informational Content (IC) of each term of annotation.
The outputs are:
1. "Ann_MIM.txt" are the valid MIM (diseases of PS with valid annotation);
2. "out_ic.txt" are the terms of annotation with their IC;
3. "Similarities.zip" are all possible pair of MIM and their value of similarity.

The second script to run is "Analysis_of_similarity.py", starting from the calculated similarities, it calculates and returns some statistics about PS.
The outputs are:
1. "Sim_mean.txt" the mean similarities among MIM in PS compared to random similarities;
2. "Sim_max.txt" the max similarities of each MIM in PS.
 
