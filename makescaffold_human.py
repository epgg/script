# takes chromInfo.txt as input


import sys

if len(sys.argv) != 2:
	print 'Require chromInfo.txt from ucsc, output to stdout'
	sys.exit()

print 'ROOT\tother\t0\nROOT\tchromosome\t0'
with open(sys.argv[1]) as fin:
	for line in fin:
		lst = line.split('\t')
		if '_' in lst[0]:
			print 'other\t{0}\t{1}'.format(lst[0],lst[1])
		else:
			print 'chromosome\t{0}\t{1}'.format(lst[0],lst[1])
