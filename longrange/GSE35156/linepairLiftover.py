import sys,os,random



if len(sys.argv) != 4:
	print '<input linepair file> <chain file> <output dir>'
	sys.exit()


infile, chainfile, outdir = sys.argv[1:]

coords = set()
with open(infile) as fin:
	for line in fin:
		lst = line.split('\t')
		coords.add(lst[0])
		coords.add(lst[1])

old2new = {}
rand = str(random.uniform(0,1))
for c in coords:
	open(outdir+rand+'x','w').write(c+'\n')
	#os.system('/home/comp/twlab/xzhou/bin/x86_64/liftOver {0}{1}x {2} {0}{1}y {0}{1}z'.format(outdir, rand, chainfile))
	os.system('liftOver {0}{1}x {2} {0}{1}y {0}{1}z'.format(outdir, rand, chainfile))
	lst = open(outdir+rand+'y').readlines()
	if len(lst)==1:
		old2new[c] = lst[0].rstrip().replace('\t',' ')

fout = open(outdir+os.path.basename(infile),'w')
with open(infile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		if lst[0] in old2new and lst[1] in old2new:
			fout.write('{0}\t{1}\t{2}\n'.format(old2new[lst[0]], old2new[lst[1]], lst[2]))
fout.close()
