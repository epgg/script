import sys
import glob
import os.path

if len(sys.argv) != 3:
	print "Usage: {0} <old trackAnnotation table upload file> <dir with separate files> output to stdout".format(sys.argv[0])
	sys.exit()


oldfile, indir = sys.argv[1:]


anno = {} # key: track name, val: set of attribute id
with open(oldfile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		if len(lst) != 2:
			print 'track with no annotation: '+lst[0]
			sys.exit()
		lst2 = lst[1].split(',')
		anno[lst[0]] = set(lst2)

for f in glob.glob(os.path.join(indir, '*')):
	with open(f) as fin:
		for line in fin:
			lst = line.rstrip().split('\t')
			if len(lst) != 2:
				print 'track with no annotation: '+lst[0]
				sys.exit()
			lst2 = lst[1].split(',')
			if lst[0] not in anno:
				anno[lst[0]] = set(lst2)
			else:
				for i in lst2:
					anno[lst[0]].add(i)

# output
for k,s in anno.items():
	print '{0}\t{1}'.format(k, ','.join(list(s)))
