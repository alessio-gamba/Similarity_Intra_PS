Here a short explication on the use of files provided.
The two scripts, Sim_calc.py and Analysis.py are written for Python 3, but with minor changes can work also in Python 2.
The first script needs 3 input files:
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
