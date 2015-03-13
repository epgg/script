import sys


if len(sys.argv) != 4:
	print 'Usage: <metadataVocabulary file> <attr name (must not be leaf term)> <trackAnnotation file>'
	sys.exit()

mvFile = sys.argv[1]
queryIdx = sys.argv[2]
annoFile = sys.argv[3]


p2c = {}
with open(mvFile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		if lst[1] in p2c:
			p2c[lst[1]].append(lst[0])
		else:
			p2c[lst[1]] = [lst[0]]
if queryIdx not in p2c:
	print '{0} not a parent'.format(queryIdx)
	sys.exit()


def getChild(what, tset):
	if what in p2c:
		for x in p2c[what]:
			getChild(x, tset)
	else:
		tset.add(what)

def countNumber(what):
	tset = set()
	getChild(what, tset)
	tknum = 0
	notin = []
	with open(annoFile) as fin:
		for line in fin:
			notfound = True
			lst = line.rstrip().split('\t')
			lst2 = lst[1].split(',')
			for idx in lst2:
				if idx in tset:
					tknum += 1
					notfound = False
					break
			if notfound:
				notin.append(lst[0])
	return [tknum, notin]


totalN = 0
with open(annoFile) as fin:
	for line in fin:
		totalN += 1
print 'Total #: {0}'.format(totalN)
res = countNumber(queryIdx)
print 'Parent \'{0}\' got {1}'.format(queryIdx, res[0])
#print 'not of parent: {0}\n'.format(res[1])
for cidx in p2c[queryIdx]:
	print 'Child \'{0}\' got {1}'.format(cidx, countNumber(cidx)[0])
