# add gene count and GC content to contig length file
import sys

if len(sys.argv) != 4:
	print 'Usage: {0} <raw contig size file> <refgene.txt> <gc content file> output to stdout'.format(sys.argv[0])
	sys.exit()

clen = {}
cnum = {}
with open(sys.argv[1]) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		clen[lst[0]] = lst[1]
		cnum[lst[0]] = 0
gc = {}
with open(sys.argv[3]) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		gc[lst[0]] = lst[1]


with open(sys.argv[2]) as fin:
	for line in fin:
		lst = line.split('\t')
		if lst[2] in clen:
			cnum[lst[2]] += 1

for c in clen:
	print '{0}\t{1}\t{2}\t{3}'.format(c, clen[c], cnum[c], gc[c])
