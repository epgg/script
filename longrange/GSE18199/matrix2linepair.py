import sys,glob,os


if len(sys.argv) != 4:
	print '<input directory, one .txt file for each map (could be either intra- or inter-chromosome> <chr size file> <output linepair file>'
	sys.exit()


indir,chrsizefile,outfile = sys.argv[1:]

'''
chrsize = {}
with open(chrsizefile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		chrsize[lst[0]] = int(lst[1])
		'''


fout = open(outfile,'w')

for f in glob.glob(sys.argv[1]+'*'):
	bn = os.path.basename(f)
	with open(f) as fin:
		fin.readline()
		lst = fin.readline().strip().split('\t')
		columnlst = [x.split('|')[2] for x in lst]
		for line in fin:
			lst = line.rstrip().split('\t')
			coord = lst[0].split('|')[2]
			i=0
			for ss in lst[1:]:
				if float(ss) != 0:
					fout.write('{0}\t{1}\t{2}\n'.format(coord, columnlst[i], ss))
				i += 1
fout.close()
