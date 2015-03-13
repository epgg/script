# convert chiapet "bed" files downloaded from ucsc database to bed then index by tabix

import sys, os

if len(sys.argv) != 3:
	print 'Usage: {0} <input> <track name (basename of output file)>'.format(sys.argv[0])
	sys.exit()

def topos(string):
	t = string.split(':')
	t2 = t[1].split('-')
	return (t[0], int(t2[0]), int(t2[1]))


infile,outfile = sys.argv[1:]
fout = open(outfile, 'w')
n = 1
data={}
with open(infile) as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		x = lst[3].split(',')
		# x[1] is pet count
		t = x[0].split('-')
		ps1 = t[0].replace('..','-')
		ps2 = t[1].replace('..','-')
		p1 = topos(ps1)
		p2 = topos(ps2)

		this=lst[0]+':'+lst[1]+'-'+lst[2]
		that= ps2 if this==ps1 else ps1
		if this in data and data[this]==that:
			continue
		data[that]=this

		p1aheadp2 = None
		if p1[0] == p2[0]:
			if p1[1] > p2[1]:
				p1aheadp2 = False
			else:
				p1aheadp2 = True
			fout.write('{0[0]}\t{0[1]}\t{0[2]}\t{1},{2}\t{3}\t{4}\n'.format(p1, ps2, x[1], n, '+' if p1aheadp2 else '-'))
			n+=1
			fout.write('{0[0]}\t{0[1]}\t{0[2]}\t{1},{2}\t{3}\t{4}\n'.format(p2, ps1, x[1], n, '-' if p1aheadp2 else '+'))
			n+=1
		else:
			fout.write('{0[0]}\t{0[1]}\t{0[2]}\t{1},{2}\t{3}\t.\n'.format(p1, ps2, x[1], n))
			n += 1
			fout.write('{0[0]}\t{0[1]}\t{0[2]}\t{1},{2}\t{3}\t.\n'.format(p2, ps1, x[1], n))
			n += 1
fout.close()


os.system('bedSort {0} {0}'.format(outfile))
os.system('bgzip {0}'.format(outfile))
os.system('tabix -p bed {0}.gz'.format(outfile))

