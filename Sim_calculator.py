from collections import Counter
from math import log
from random import sample
from itertools import combinations
from time import clock
t0 = clock()

##########################################
# open, read and close the given file
def Open_r(infile):
	f = open(infile,'r')
	inp = f.readlines()
	f.close()
	return inp

# invert key-value of dictionary
def Invert(D1):
	D2 = dict()
	for key in D1:
		D2[key]=[]
	for key in D1:
		for val in D1[key]:
			D2[val].append(key)
	return D2

# calculates from a given term descendants or ancestors,
# depending by the dictionary used.
def Descendant(parent, D): # D is the disctionary to use
	desc = set(parent) # set with descendants
	while parent != set([]): # when a parent has no childs (end reached)
		child = [] # all children of the parent are put in this list
		for term in parent:
			child.extend(D[term])
		parent = set(child) # children become the new parents
		desc = desc | parent
	return desc

# calculates from a given term descendants or ancestors,
# depending by the dictionary used.
def Ancestor(child, D): # D is the disctionary to use
	level = 0 # counter of the level
	anc = set(child) # set with descendants
	while child != set([]): # when a parent has no childs (end reached)
		level += 1 # counter +1
		parent = [] # all children of the parent are put in this list
		for term in child:
			parent.extend(D[term])
		child = set(parent) # children become the new parents
		anc = anc | child
	return [anc, level]
	
###############################################

# Open and read the entire ontology.
infile = open('hp.obo','r') # open the file "hp.obo"
inp = infile.read() # read it
infile.close() # and close it

D_hp_name = dict() # create a dictionary for the names of hpo terms
D_hpo = dict() # create a dictionary for all terms
inp = inp.split('[Term]\n')[1:] # split each term and skip all before the first "[Term]" (file header)
for term in inp:
	term = term.split('\n')
	ID = term[0][4:] # the term ID, as "HP:0000001"
	parent = [] # create a list for parents of the term
	for line in term:
		if line.startswith("name:"): # name of the term
			D_hp_name[ID] = line[6:] # add name to the dictionary
		elif line.startswith("is_a:"): # "is_a" indicates the parent
			parent.append(line[6:16]) 
	if parent != []: # if the list of parents is no empty
		D_hpo[ID] = parent # the dictionary for each term has a list of its parents

D_hpo["HP:0000001"] = [] # add the root that has no parent
print "number of total HPO terms:", len(inp)
print "number of HPO terms (removing obsolete):", len(D_hpo)

D_hpo2 = Invert(D_hpo)

son118 = Descendant(['HP:0000118'], D_hpo2) # calculate the descendants
print "HPO terms descendant of HP:0000118 are:", len(son118)


D_hpo3 = dict() # new dictionary of HPO with only descendant of 118
for key in son118:
	parent = set(D_hpo[key]) & son118 # keep only parents that are also valid
	D_hpo3[key] = list(parent)

D_hpo.clear() 
D_hpo2.clear() # cancel hpo and hpo2, only hpo3 is used

D_IC = dict() # dictionary with Inform. Content
D_Anc = dict() # dictionary of all ancestors for each terms
All = [] # a list with all ancestors
for term in son118:
	Anc = Ancestor([term], D_hpo3) # calculate the ancestors
	D_Anc[term] = Anc[0] # the set of ancestors
	All.extend(Anc[0]) 
	D_IC[term] = Anc[1]-1 # the distance is the level minus one

D_count = Counter(All) # count the presence of each term

max1 = float(max(D_IC.values())) # max distance from root
N = float(len(D_Anc)) # number of terms
max2 = -log(1/N) # maximal possible value when freq=1/N

for term in son118:
	ndis = D_IC[term]/max1 # normalized distance
	nlog = -log(D_count[term]/N)/max2 # normalized logarithm
	D_IC[term] = (ndis+nlog)/2.0 # the medium value between length and logarithm

D_count.clear()

# combine the two dictionaries
D_Anc2 = dict()
for term in son118:
	Anc = []
	for v in D_Anc[term]:
		Anc.append((D_IC[v], v))
	D_Anc2[term] = set(Anc)

D_IC.clear()
D_Anc.clear()

########## comment this #############
L=[]
for i in range(100):
	sam = sample(son118, 2)
	t1 = sam[0]
	t2 = sam[1]
	sim = max(D_Anc2[t1] & D_Anc2[t2])
	L.append(sim[0])
sim = sum(L)/len(L)
print "Similarity between two random terms is:", sim
########## comment this #############


# open and extract information from the file "Annotation"
inp = Open_r("OMIM_ALL_FREQUENCIES_diseases_to_genes_to_phenotypes.txt")
D_mim2hp = dict() # dictionary with omim and respective hp terms 
for line in inp[1:]: # skip first line (file header)
	line = line.split('\t')
	hp = line[3]
	if hp not in son118: # term not descendants of 118
		continue
	mim = line[0][5:]
	try:
		D_mim2hp[mim].add(hp)
	except KeyError:
		D_mim2hp[mim] = set([hp])

annotated = set(D_mim2hp.keys())
print "Annotated MIM are:", len(annotated)

# open and extract information from the file "PhenSer"
inp = Open_r("PhenSer.txt")
valid = set()
for line in inp:
	line = line.split('\t')
	valid.add(line[1]) # MIM

valid = valid & annotated
print "Annotated MIM in PS are:", len(valid)	

out1 = open('Ann_MIM.txt', 'w')
for mim in valid:
	out1.write(mim + '\n')
out1.close()

############################################
########### calculate similarity ###########

D_mim2anc1 = dict() # from mim to hp-ancestors separated for each hp
D_mim2anc2 = dict() # from mim to hp-ancestors of all hp together
for mim in valid: # valid diseases
	anc1 = []
	anc2 = []
	for hp in D_mim2hp[mim]:
		anc1.append(D_Anc2[hp])
		anc2.extend(list(D_Anc2[hp]))
	D_mim2anc1[mim] = anc1
	D_mim2anc2[mim] = set(anc2)

D_mim2hp.clear()
D_Anc2.clear()

Com = list(combinations(valid, 2))
print 'All combinations are:', len(Com)

D_sim = dict()
for d1,d2 in Com:
	mica = []
	for val in D_mim2anc1[d1]:
		M = max(val & D_mim2anc2[d2])
		mica.append(M[0])
	for val in D_mim2anc1[d2]:
		M = max(val & D_mim2anc2[d1])
		mica.append(M[0])
	sim = sum(mica)/len(mica)
	D_sim[(d1, d2)] = sim

out2 = open('All_Sim_PS.txt', 'w')
for k in D_sim:
	sim = D_sim[k]
	out2.write('%s\t%s\t%.5f\n' % (k[0], k[1], sim))
out2.close()


#################
t1 = clock()
print "Elapsed time:", t1 - t0
#################

