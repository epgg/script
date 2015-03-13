import sys

if len(sys.argv)!=3:
	print '<cateinfo file> <rmsk.txt> output to stdout'
	sys.exit()


cateinfile, rmskfile=sys.argv[1:]

cateinfo={}

with open(cateinfile) as fin:
	for line in fin:
		lst=line.rstrip().split()
		cateinfo[lst[0]]=lst[1]


with open(rmskfile) as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		if lst[11] in cateinfo:
			print '{0}\t{1}\t{2}\t{3}'.format(lst[5],lst[6],lst[7],cateinfo[lst[11]])
