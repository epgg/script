import sys,random,os

if len(sys.argv) != 3:
	print 'Usage: {0} <chromsome size file> <output bigwig file>'.format(sys.argv[0])
	sys.exit()

# random value every 20bp

fout = open('xxx', 'w')
with open(sys.argv[1]) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		clen = int(lst[1])
		print lst[0]
		fout.write('fixedStep chrom={0} start=1 step=100 span=100\n'.format(lst[0]))
		a = 1
		while a+100 < clen:
			a += 100
			fout.write('{:.2f}\n'.format(random.normalvariate(0,10)))
fout.close()

os.system('wigToBigWig xxx {0} {1}'.format(sys.argv[1], sys.argv[2]))

os.unlink('xxx')
