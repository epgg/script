import sys


if len(sys.argv) == 1:
	print "usage: {0} <trackDetail table load file> <trackAttr2idx table load file> <attribute name like donor_id>\noutput to stdout".format(sys.argv[0])
	sys.exit()

infile, infile2, attr = sys.argv[1:]


# load trackAttridx
attr2idx = {} # key: attr name, value: id
with open(infile2) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		attr2idx[lst[1].lower()] = lst[0]



# parse trackDetail, abort on none-existing attribute names
sep = attr+'='
unknown = set()
with open(infile) as fin:
	for line in fin:
		lst = line.split('\t')
		if len(lst) != 4:
			print 'one line doesn\'t have 4 fields'
			sys.exit()
		if sep not in lst[2]:
			continue
		messy = lst[2].split(attr+'=')[1]
		word = ''
		if messy[0] == '"':
			word = messy[1:].split('"')[0]
		else:
			word = messy.split()[0]
		wordl = word.lower()
		if wordl not in attr2idx:
			unknown.add(word)
			#sys.stderr.write('{0} ===> {1}\n'.format(word, lst[2]))
			#sys.exit()
		else:
			print '{0}\t{1}'.format(lst[0], attr2idx[wordl])
if len(unknown) > 0:
	for u in unknown:
		print u
