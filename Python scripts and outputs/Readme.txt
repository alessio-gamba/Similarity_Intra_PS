Here a short explication on the use of files provided.
The two Python scripts, Sim_calc.py and Analysis_of_similarity.py, produce the outputs provided in this folder.
The scripts are written for Python 3, but they work also in Python 2, with few minor changes.

INPUT
"hp.obo"
This file is the Human Phenotype Ontology (HPO) in obo format.
It is not provided here because it is freely available at HPO site.

"OMIM_ALL_FREQUENCIES_diseases_to_genes_to_phenotypes.txt"
This file provides OMIM diseases with their terms of annotations (one or more terms for each disease).
It is not provided here because it is freely available at

"PhenSer.txt"
This file enlists Phenotypic Series (PS) of OMIM with their associated diseases (with MIM code).
The file must be formatted in 4 columns tab-separated, that are: The PS identifier,	the MIM identifier, the Entrez identifier of the gene associated to disease and the Symbol of the Entrez. Here an example of the PS 174050 formed by 3 diseases:

PS174050	174050	5589	PRKCSH
PS174050	617875	4041	LRP5
PS174050	617874	79053	ALG8


The first script to run is Sim_calc.py, it requires 3 input files:
1. the hp.obo is the human phenotype ontology
2. the file with annotated diseases (MIM code)
3. the file with Phenotypic Series.

The first script calculates and print as txt output 3 files:
1. the informational content of used hp term
2. the list of valid MIM
3. the file enlisting all possible pair of MIM and their value of similarity

The second script needs as input:
1. the list of all similarities
2. the list of valid MIM
3. the file with Phenotypic Series.

It calculates some statistics, returned in two files:
1. the mean similarities in PS
2. the max similarities of each MIM
