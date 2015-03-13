import sys

if len(sys.argv) != 2:
	print "require wgRna.txt file, output to stdout"
	sys.exit()


i = 0
with open(sys.argv[1]) as fin:
	for line in fin:
		lst = line.split('\t')
		print '{0[1]}\t{0[2]}\t{0[3]}\t{0[6]}\t{0[4]}\t{1}'.format(lst, i)
		i += 1
