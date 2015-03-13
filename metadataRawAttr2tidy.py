import sys

if len(sys.argv) != 2:
	print "Require metadata raw attribute file, rows starting with ### are notes, else it will be treated as a value, output to stdout"
	sys.exit()


# output file:
# 1. attribute string
# 2. index
# 3. note
note = ''
idx = 1
with open(sys.argv[1]) as fin:
	for line in fin:
		if line.startswith('###'):
			note = line.rstrip().split()[1]
		else:
			# expect lines line "| liver    |"
			line = line.strip()
			if line[0] == '|':
				line = line[1:]
			if line[-1] == '|':
				line = line[:-1]
			print "{0}\t{1}\t{2}".format(idx, line.strip(), note)
			idx += 1
