import sys


if len(sys.argv) != 3:
	print 'takes contigLength file, make it into bed file for computing GC content'
	sys.exit()


fout = open(sys.argv[2], "w")
with open(sys.argv[1]) as fin:
	for line in fin:
		lst = line.split('\t')
		fout.write('{0}\t0\t{1}\n'.format(lst[0], lst[1]))


fout.close()
