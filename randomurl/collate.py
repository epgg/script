import random
import sys

collatelst = ['cpgisland','DNA','exons','genebody','introns','LINE','Low_complexity','LTR','Other','promoter','RNA','Satellite','Simple_repeat','SINE','Unknown','utr3','utr5']

tracklst = []
with open('/home/xzhou/subtleKnife/config/hg19/trackDetail') as fin:
	for line in fin:
		tracklst.append(line.split('\t')[0])


chrlst = [] # each ele: [name, length]
with open('/home/xzhou/data/hg19/chr_len2') as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		chrlst.append([lst[0], int(lst[1])])


span = 3000000

# random URL
for i in range(10000):
	sys.stdout.write("http://epigenomegateway.wustl.edu/cgi-bin/subtleKnife?first=on&changeGF=on&session=xxxxxx")
	sys.stdout.write("&gftype="+random.sample(collatelst,1)[0])
	chrom = random.sample(chrlst, 1)[0]
	sys.stdout.write("&startChr="+chrom[0])
	start = int(random.uniform(1, chrom[1]-span))
	sys.stdout.write("&startCoord="+str(start))
	sys.stdout.write("&stopChr="+chrom[0])
	sys.stdout.write("&stopCoord="+str(start+span))
	# # of tracks range from 50 to 150
	tkn = int(random.uniform(50,150))
	tkset = set()
	for j in range(tkn):
		tkset.add(random.sample(tracklst, 1)[0])
	for n in tkset:
		sys.stdout.write("&{0}=on".format(n))
	print
