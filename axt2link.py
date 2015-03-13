# ucsc axtNet files to Link files

import glob

flst=glob.glob('*')

for fn in flst:
	with open(fn) as fin:
		for line in fin:
			if line[0]=='#': continue
			lst=line.rstrip().split()
			if len(lst)!=9: continue
			print '{0}\t{1}\t{2}\t{3} {4} {5} {6}'.format(lst[1],lst[2],lst[3],lst[4],lst[5],lst[6],lst[7])
