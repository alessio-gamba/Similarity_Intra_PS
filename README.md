The datasets reported in the enclosed files have been generated and analyzed, as described in the manuscript entitled ‘The Similarity of Inherited Diseases (I): Clinical Similarity Within the Phenotypic Series’ by Gamba A, Salmona M and Bazzoni G (Submitted to BMC Medical Genomics, Revised December 4, 2020)

A. SQL folder

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

 
  B. Python code:
  
  The first script is 'Sim_calculator.py' (running under Python 2).
  
  It generates a very big file (58 MB) with similarities calculated between all the possible pairs of OMIM Diseases.
  Similarities are calculated based on the HPO annotation of diseases.
  The file with similarities is necessary to proceed in the analysis.

  The second script is 'Analysis_of_similarity.py' (running under Python 2).
  
  It generates two files: 'Sim_mean.txt' and 'Sim_max.txt' (now in the outputs folder).

  The two Python scripts require three input files (not provided here, but publicly available):
  
  1. hp.obo
  
  2. OMIM_ALL_FREQUENCIES_diseases_to_genes_to_phenotypes.txt
  
  3. PhenSer.txt
  
  Files 1 and 2 are the HPO ontology and the list of diseases with their terms of annotation, respectively. They can be downloaded from the HPO web site.
  
  File 3 indicates how some OMIM diseases are grouped in Phenotypic Series. It is available from the OMIM team upon request.
