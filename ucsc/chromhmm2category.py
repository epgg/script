import sys



if len(sys.argv) != 2:
	print 'Require input file, output to stdout'
	sys.exit()



with open(sys.argv[1]) as fin:
	for line in fin:
		lst=line.split('\t')
		print '{0}\t{1}\t{2}\t{3}'.format(lst[1],lst[2],lst[3],lst[4].split('_')[0])
