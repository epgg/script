import sys,glob,os,gzip


if len(sys.argv) != 4:
	print '<input directory, one .gz file for each chromosome> <chr size file> <output linepair file>'
	sys.exit()


indir,chrsizefile,outfile = sys.argv[1:]

chrsize = {}
with open(chrsizefile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		chrsize[lst[0]] = int(lst[1])


fout = open(outfile,'w')

for f in glob.glob(sys.argv[1]+'*'):
	bn = os.path.basename(f)
	fin = gzip.open(f)
	coordlst = []
	for line in fin:
		lst = line.split('\t',3)
		stop = int(lst[2])
		stop = chrsize[lst[0]] if stop>chrsize[lst[0]] else stop
		coordlst.append((lst[0],lst[1],str(stop)))
	fin.seek(0)
	print 'processing '+f+' ...'
	j = 0
	for line in fin:
		lst = line.rstrip().split('\t')
		i = 0
		for v in lst[3:]:
			if float(v) > 0:
				fout.write('{0[0]} {0[1]} {0[2]}\t{1}\t{2}\n'.format(coordlst[j], ' '.join(coordlst[i]), v))
			i += 1
		j += 1
	fin.close()
fout.close()
