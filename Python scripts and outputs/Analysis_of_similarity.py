from collections import Counter
#from math import log
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

###############################################
inp = Open_r("Ann_MIM.txt") # annotated mim
valid = set()
for line in inp:
	line = line[:-1]
	valid.add(line) # mim present in PS and annotated

inp = Open_r("PhenSer.txt")
D_PS_m = dict() # dictionary PS to MIM
#D_m_PS = dict() # dictionary with omim and associated gene (or genes)
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
	#try:
	#	D_m_PS[mim].add(PS)
	#except KeyError:
	#	D_m_PS[mim] = set([PS])

# open and create a dictionary from the similarity output
inp = Open_r('All_Sim_PS.txt')
D_sim = dict()
for line in inp:
	line = line[:-1].split('\t')
	D_sim[(line[0], line[1])] = float(line[2])


'''
# calculate the mean sim among all sim
sim = D_sim.values()
mean = sum(sim)/len(sim)
print 'The mean of all similarities is:', mean
D_count = Counter(sim)
print len(D_count)
for el in D_count:
	if D_count[el] > 900:
		print el, D_count[el]
'''

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
	
D_mean = dict() # mean similarities
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
		for c in range(1000):
			rs = sample(D_omim2[i], n-1) # random similarity
			mean.append(sum(rs)/(n-1))
		
		m4 = sum(mean)/len(mean)
		
		out1.write("%s\t%d\t%s\t%.4f\t%.4f\t%.4f\t%.4f\n" % (ps, n, i, m1, m2, m3, m4))
		
out1.close()

D_max = dict() # max similarity
for k in D_omim1:
	val = D_omim1[k]
	val.sort(reverse=True)
	m = val[0][0]
	D_max[k] = [m]
	for el in val:
		if el[0] == m: # if similarity is = to max sim.
			D_max[k].append(el[1]) # append the omim with max sim.
		else:
			break
			
out2 = open('Sim_max.txt', 'w')
for ps in D_PS_m:
	for mim in D_PS_m[ps]:
		val = D_max[mim]
		for el in val[1:]:
			out2.write("%s\t%s\t%.4f\t%s\n" % (ps, mim, val[0], el))
	
out2.close()

#################
t1 = clock()
print "Elapsed time:", t1 - t0
#################


