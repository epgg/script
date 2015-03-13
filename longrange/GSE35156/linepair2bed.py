import sys,os


if len(sys.argv) != 2:
	print 'input linepair file, output to same directory'
	sys.exit()



infile = sys.argv[1]


fout = open(infile+'.bed','w')
with open(infile) as fin:
	i = 0
	for line in fin:
		lst = line.rstrip().split('\t')
		c1 = lst[0].split()
		c2 = lst[1].split()
		fout.write('{0[0]}\t{0[1]}\t{0[2]}\t{1[0]}:{1[1]}-{1[2]},{2}\t{3}\t{4}\n'.format(
			c1,c2,
			lst[2],
			i,
			'.' if c1[0]!=c2[0] else ('+' if int(c1[1])<int(c2[1]) else '-')))
		i += 1
fout.close()
