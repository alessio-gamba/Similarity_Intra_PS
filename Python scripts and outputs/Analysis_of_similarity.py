from collections import Counter
from random import sample
#from itertools import combinations



# This opens the file with all valid MIMs
inp = open("Ann_MIM.txt",'r').readlines() # annotated MIMs
valid = set()
for line in inp:
  line = line[:-1]
  valid.add(line) # valid = MIMs in PS and also annotated



# This opens the file with Phenotypic Series and their MIMs
inp = open("PhenSer.txt",'r').readlines()
D_PS_m = dict() # dictionary PS to MIM
for line in inp:
  line = line.split('\t')
  mim = line[1] # MIM
  if mim not in valid:
    continue
  PS = line[0]
  try:
    D_PS_m[PS].add(mim)
  except KeyError:
    D_PS_m[PS] = set([mim])



# This opens the file with all similarities previously calculated
infile = open("All_Sim_PS.txt",'r')
inp = infile.readlines()
infile.close()
D_sim = dict() # this creates a dictionary with all similarities 
for line in inp:
  line = line[:-1].split('\t')
  D_sim[(line[0], line[1])] = float(line[2])



D_omim1 = dict()
D_omim2 = dict()
for k in valid:
  D_omim1[k]=[]
  D_omim2[k]=[]
  
for k in D_sim:
  sim = D_sim[k] # similarity between d1 and d2
  D_omim1[k[0]].append((sim, k[1])) # disease 1
  D_omim1[k[1]].append((sim, k[0])) # disease 2
  D_omim2[k[0]].append(sim) # disease 1
  D_omim2[k[1]].append(sim) # disease 2
  
  

  
# mean similarities

D_mean = dict()
for k in D_omim2:
  val = D_omim2[k]
  D_mean[k] = sum(val)/len(val) # mean of all

out1 = open('Sim_mean.txt', 'w')

for ps in D_PS_m:
  val = D_PS_m[ps]
  n = len(val)
  for i in val: # mim_i
    m1 = D_mean[i] # mean 1
    if n == 1:
      out1.write("%s\t%d\t%s\t%.4f\t--\t--\t--\n" % (ps, n, i, m1))
      continue
    Lsim = []
    for j in val:
      if i == j:
        continue
      try:
        sim = D_sim[(i,j)]
      except KeyError:
        sim = D_sim[(j,i)]
      Lsim.append(sim) # list of similarities
    
    m2 = sum(Lsim)/len(Lsim) # real mean
    rs = sample(D_omim2[i], n-1) # rs: random sample
    m3 = sum(rs)/(n-1)

    mean = []
    for c in range(10000): # change this value for more simulations 
      rs = sample(D_omim2[i], n-1) # random similarity
      mean.append(sum(rs)/(n-1))
    
    m4 = sum(mean)/len(mean)
    
    out1.write("%s\t%d\t%s\t%.4f\t%.4f\t%.4f\t%.4f\n" % (ps, n, i, m1, m2, m3, m4))
    
out1.close()




# max similarity

D_max = dict()
for k in D_omim1:
  val = D_omim1[k]
  val.sort(reverse=True)
  m = val[0][0]
  D_max[k] = [m]
  for el in val:
    if el[0] == m: # if similarity is = to max similarity
      D_max[k].append(el[1]) # append the MIM with max similarity
    else:
      break
      
out2 = open('Sim_max.txt', 'w')
out2.write("PS_ID\tMIM\tmax_similarity\twith_MIM\n")

for ps in D_PS_m:
  for mim in D_PS_m[ps]:
    val = D_max[mim]
    for el in val[1:]:
      out2.write("%s\t%s\t%.4f\t%s\n" % (ps, mim, val[0], el))
  
out2.close()


