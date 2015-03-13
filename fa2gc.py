import sys


if len(sys.argv) != 3:
	print 'Usage: {0} <input .fa> <out file> compute GC content for each sequence'.format(sys.argv[0])
	sys.exit()



letters = set(["g", "G", "c", "C"])

fout = open(sys.argv[2], "w")
with open(sys.argv[1]) as fin:
	gc = 0
	totallen = 0
	name = ''
	for line in fin:
		if line[0] == '>':
			if name != '':
				fout.write("{0}\t{1}\n".format(name, float(gc)/totallen))
			name = line.rstrip()[1:]
			gc = 0
			totallen = 0
		else:
			seq = line.strip()
			totallen += len(seq)
			for i in range(len(seq)):
				if seq[i] in letters:
					gc += 1


fout.write("{0}\t{1}\n".format(name, float(gc)/totallen))
fout.close()
