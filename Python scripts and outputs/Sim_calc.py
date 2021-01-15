from collections import Counter
from math import log
from itertools import combinations


def Open_obo(obo_infile):
  infile = open(obo_infile,'r') # open the file "hp.obo"
  inp = infile.read()
  infile.close()
  inp = inp.split('\n\n')
  D_hpo = dict()
  for term in inp:
    term = term.split('\n')
    if term[0] != '[Term]':
      continue
    parents = []
    for line in term:
      if line.startswith("id: "):
        ID = line[4:] # the term ID, as "HP:0000001"
      elif line.startswith("is_a:"): # "is_a" indicates one parent
        parents.append(line[6:16])
    D_hpo[ID] = parents
  return D_hpo



def Invert_d(D1):
  D2 = dict()
  for key,val in D1.items():
    D2[key]=[]
  for key,val in D1.items():  
    for v in val:
      D2[v].append(key)
  return D2

  

def Sub_ontology(parents, D1):
  D2=dict()
  while parents != set([]):
    sons = []
    for term in parents:
      D2[term] = D1[term]
      sons.extend(D1[term])
    parents = set(sons)
  return D2

      

def Calc_ancestors(sons, D_hpo): # D is the disctionary to use
  level = 0 # counter of the level
  anc = sons # set with descendants
  while sons != set([]): # when a parent has no childs (end reached)
    level += 1 # counter +1
    parents = [] # all children of the parent are put in this list
    for term in sons:
      parents.extend(D_hpo[term])
    sons = set(parents) # children become the new parents
    anc.extend(sons)
  return (set(anc), level-1) # distance = level-1



def D_ancestors(D_hpo):
  D_Anc = dict()
  D_Lev = dict() # dictionary of all ancestors for each terms
  for term in D_hpo.keys():
    (anc, lev) = Calc_ancestors([term], D_hpo)
    D_Anc[term] = anc
    D_Lev[term] = lev
  return (D_Anc,D_Lev)



def Count_ancestors(D_Anc):
  all_anc=[]
  for val in D_Anc.values():
    all_anc.extend(val)  
  D_count = Counter(all_anc)
  return D_count



def Calc_ic(D_Anc,D_Lev,D_count):
  max_lev = max(D_Lev.values()) # max distance from root
  N = len(D_Anc) # number of terms
  max_log = -log(1/N) # maximal possible value when freq=1/N
  D_IC = dict()
  for term in D_Anc.keys():
    norm_lev = D_Lev[term] / max_lev # normalized level (or distance from root)
    norm_log = -log(D_count[term]/N) / max_log # normalized logarithm
    D_IC[term] = (norm_lev+norm_log) / 2 # the medium value between length and logarithm
  return D_IC



def Join_anc_ic(D_Anc, D_IC):
  D = dict()
  for term, val in D_Anc.items():
    D[term] = set([(D_IC[v],v) for v in val])
  return D
  


def Open_annotation(infile,valid_hp):
  f = open(infile,'r')
  inp = f.readlines()
  f.close()
  D_mim2hp = dict()
  for line in inp[1:]: # skip first line (file header)
    line = line.split('\t')
    hp = line[3]
    if hp not in valid_hp:
      continue
    mim = line[0][5:]
    try:
      D_mim2hp[mim].add(hp) 
    except KeyError:
      D_mim2hp[mim] = set([hp])
  return D_mim2hp # dictionary with omim and respective hp terms 



def Open_PS(infile):
  inp = open(infile,'r').readlines()
  return set([line.split('\t')[1] for line in inp])



#########################################

D_hpo = Open_obo('hp.obo')
D_hpo = Invert_d(D_hpo)
D_hpo = Sub_ontology(['HP:0000118'],D_hpo)
D_hpo = Invert_d(D_hpo)
print("The terms of sub-ontology (with root HP:0000118) are:", len(D_hpo)) 

(D_Anc,D_Lev) = D_ancestors(D_hpo)
D_count = Count_ancestors(D_Anc)
D_IC = Calc_ic(D_Anc,D_Lev,D_count)
D_Anc2 = Join_anc_ic(D_Anc, D_IC)

valid_hp = set(D_IC.keys())
D_mim2hp = Open_annotation("OMIM_ALL_FREQUENCIES_diseases_to_genes_to_phenotypes.txt",valid_hp)
mim_annotated = set(D_mim2hp.keys())
mim_in_ps = Open_PS("PhenSer.txt") # read only the mim present in PS file
valid = mim_in_ps & mim_annotated # valid MIM
print("Diseases (MIM) annotated in Phenotypic Series are:", len(valid))


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





##### print IC as output ##### 
out1 = open('out_ic.txt','w')
for k,v in D_IC.items():
  out1.write('%s\t%.4f\n' % (k,v))
out1.close()

##### print valid MIM #####
out2 = open('Ann_MIM.txt', 'w')
for mim in valid:
  out2.write('%s\n' % mim)
out2.close()

##### print sim as output #####
out3 = open('All_Sim_PS.txt', 'w')
for k,sim in D_sim.items():
  out3.write('%s\t%s\t%.5f\n' % (k[0], k[1], sim))
out3.close()


