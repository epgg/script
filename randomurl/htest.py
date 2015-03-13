import random
import sys


tracklst = []
with open('/home/xzhou/subtleKnife/config/trackDetail') as fin:
	for line in fin:
		tracklst.append(line.split('\t')[0])


chrlst = [] # each ele: [name, length]
with open('/home/xzhou/data/hg19/chr_len2') as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		chrlst.append([lst[0], int(lst[1])])


span = 30000
spnum = [i+1 for i in range(100)]

for i in range(10000):
	startcoord = 0
	stopcoord = 0
	sys.stdout.write("http://epigenome.wustl.edu/cgi-bin/subtleKnife?session=xxxxxx&htest=on&regionLst=")
	# first region
	chrom = random.sample(chrlst, 1)[0]
	start = int(random.uniform(1, chrom[1]-span))
	sys.stdout.write("{0},{1},{2},{3},".format(chrom[0], start, start+span, random.sample(spnum, 1)[0]))
	startcoord = start
	for j in range(100):
		chrom = random.sample(chrlst, 1)[0]
		start = int(random.uniform(1, chrom[1]-span))
		sys.stdout.write("{0},{1},{2},{3},".format(chrom[0], start, start+span, random.sample(spnum, 1)[0]))
		stopcoord = start+span
	sys.stdout.write("&startCoord="+str(startcoord))
	sys.stdout.write("&stopCoord="+str(stopcoord))
	# # of tracks range from 50 to 150
	tkn = int(random.uniform(50,150))
	tkset = set()
	for j in range(tkn):
		tkset.add(random.sample(tracklst, 1)[0])
	tklst = list(tkset)
	a = len(tklst)/2
	for j in range(a):
		sys.stdout.write("&{0}=1".format(tklst[j]))
	for j in [k+a for k in range(a)]:
		sys.stdout.write("&{0}=2".format(tklst[j]))
	print
