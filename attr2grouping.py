import sys

if len(sys.argv) != 2:
	print 'require output of trackDb2attr.py, output to stdout'
	sys.exit()


with open(sys.argv[1]) as fin:
	for line in fin:
		lst = line.split('\t')
		mm = ''
		if lst[2] != '\\N':
			mm = lst[2]
		elif lst[3] != '\\N':
			mm = lst[3]
		elif lst[4] != '\\N':
			mm = lst[4]
		else:
			print line,
			sys.exit()
		print '{0}\t{1}\t{2}\t{3}'.format(lst[0], lst[1], mm, lst[8])
