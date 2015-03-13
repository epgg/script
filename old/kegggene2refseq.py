keggfile = '/home/xzhou/data/kegg/h.sapiens.pos'
# input file: h.sapiens.pos
# ftp://ftp.genome.jp/pub/kegg/genes/organisms/hsa/h.sapiens.pos
# mapping of (truncated) kegg gene id to untidy refseq name

refseqfile = '/home/xzhou/data/hg19/refGene.txt'


# output: kegg gene id to refseq name, uniq mapping

# make a set of refseq name:
rs = set()
with open(refseqfile) as fin:
	for line in fin:
		rs.add(line.split('\t')[12])

# read kegg file and output
with open(keggfile) as fin:
	for line in fin:
		lst = line.split('\t')
		if lst[1] != '':
			for n in lst[1].split(','):
				if n in rs:
					print 'hsa:{0}\t{1}'.format(lst[0], n)
					break
