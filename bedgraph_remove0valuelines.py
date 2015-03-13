import sys,os


if len(sys.argv)!=3:
	print '{0}: <input bedgraph file> <output dir> output to a file with same name'.format(sys.argv[0])
	sys.exit()

infile,outdir=sys.argv[1:]


outfile=os.path.join(outdir,os.path.basename(infile))
fout=open(outfile,'w')


with open(infile) as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		if len(lst)>4:
			print 'Weird line: '+line
			sys.exit()
		if lst[3]=='0': continue
		fout.write(line)

fout.close()

os.system('bgzip '+outfile)
os.system('tabix -p bed '+outfile+'.gz')
