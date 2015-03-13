import sys


fdir='/home/xzhou/subtleKnife/config/hg19/'
#fdir='/srv/epgg/data/kent/src/hg/subtleKnife/config/hg19/'
attributeFile = fdir+'trackAttr2idx'
vocabularyFile = fdir+'metadataVocabulary'
annoFile = fdir+'track2Annotation_roadmap'

def getRoot(what):
	if what in c2p:
		return getRoot(c2p[what])
	else:
		return what

idx2attr = {} 
# key: id
# value: attribute text name
with open(attributeFile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		if lst[0] in idx2attr:
			print 'duplicating attribute ID: '+lst[0]
			sys.exit()
		idx2attr[lst[0]] = lst[1]



c2p = {}
# key: child
# val: parent
phash={}
# key: parent
# val: 1

with open(vocabularyFile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		if len(lst)==1:
			print line
		c2p[lst[0]] = lst[1]
		phash[lst[1]]=1


print "Root terms:"
for p in set(c2p.values()):
	if p not in c2p:
		print p


print
print


notFound = False
for idx,attr in idx2attr.items():
	if idx not in c2p:
		print "{1}\t{0} not found in vocabulary file".format(attr, idx)
		notFound = True
if notFound:
	sys.exit()
else:
	print "All attributes show up in vocabulary file"



notFound=False
for c in c2p:
	if c not in phash:
		# this is leaf term
		if c not in idx2attr:
			print c+' not found in trackAttr2idx file'
			notFound=True
if notFound:
	sys.exit()
else:
	print 'All leaf terms have definitions'



print
print
with open(annoFile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		atidlst = lst[1].split(',')
		for idx in atidlst:
			if idx not in c2p:
				print 'Attribute id {0} not found for track {1}'.format(idx, lst[0])
				sys.exit()
print 'All annotations are valid'


'''
print
print
rootset = {}
with open(annoFile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		atidlst = lst[1].split(',')
		for idx in atidlst:
			rt = getRoot(idx)
			if rt not in rootset:
				rootset[rt] = set()
			rootset[rt].add(lst[0])
for rt in rootset:
	print '{0}\t{1}'.format(rt, len(rootset[rt]))


print
print "child-parent path for each attribute:"

for idx,attr in idx2attr.items():
	plst = []
	child = idx
	while child in c2p:
		plst.append(c2p[child])
		child = c2p[child]
	print attr,
	for p in plst:
		print '-- '+p,
	print
	'''
