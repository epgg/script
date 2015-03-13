import sys
import os


if len(sys.argv) != 4:
	print 'Usage: {0} <ZmB73_5a_WGS.gff> <ZmB73_5a_named_genes.txt> <ZmB73_5a_gene_descriptors.txt> output files written to cwd'.format(sys.argv[0])
	sys.exit()

gff3file, aliasfile, funcfile = sys.argv[1:]


gene = {}
# mRNA : [chr, strand, txstart, txstop, cdsstart, cdsstop, [exon starts], [exon stops] ]

mrna2gene = {} # mrna : gene

thismrna = None
invalidLst = []
with open(gff3file) as fin:
	for line in fin:
		lst = line.split('\t')
		if lst[2] == 'mRNA':
			thisgene = None
			thismrna = None
			lst2 = lst[8].split(';')
			for s in lst2:
				t = s.split('=')
				if t[0]=='ID':
					thismrna = t[1]
				elif t[0]=='Parent':
					thisgene = t[1]
			if thisgene is None or thismrna is None:
				invalidLst.push(line)
				continue
			mrna2gene[thismrna] = thisgene
			gene[thismrna] = ['chr'+lst[0], lst[6], lst[3], lst[4], None, None, [], []]
		elif lst[2] == 'CDS':
			if thismrna is None:
				continue
			gene[thismrna][6].append(lst[3])
			gene[thismrna][7].append(lst[4])



if len(invalidLst) > 0:
	print '!!! When parsing GFF file, "Parent" or "ID" field not found on {0} mRNA entries'.format(len(invalidLst))
	print invalidLst
	print
	print

invalidLst = []

# write that into gene structure table similar as ucsc's
fout = open('AGPv2_5a.txt','w')
for g in gene:
	# name, chrom, strand, txstart, txend, cdsstart, cdsend, exoncount, exonstarts, exonstops, 0, name2
	cdsStartLst = gene[g][6]
	cdsStopLst = gene[g][7]
	if len(cdsStartLst)==0 or len(cdsStopLst)==0:
		invalidLst.push(g)
		continue

	fout.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8},\t{9},\t0\t{0}\tcmpl\tcmpl\t{10},\n'.format(
		g, gene[g][0], gene[g][1], gene[g][2], gene[g][3], 
		min([int(x) for x in cdsStartLst]),
		max([int(x) for x in cdsStopLst]),
		len(cdsStartLst),
		','.join(cdsStartLst),
		','.join(cdsStopLst),
		','.join(['0' for i in range(len(cdsStartLst))])
		))
fout.close()

if len(invalidLst)>0:
	print '!!! When generating AGPv2_5a.txt, {0} genes have 0 cds and are skipped'.format(len(invalidLst))
	print invalidLst
	print
	print


os.system('/home/xzhou/subtleKnife/script/refGene2bed AGPv2_5a.txt AGPv2_5a /home/xzhou/data/b73_AGPv2/chromsize 0')


# load name - symbol - desc
desc = {}
with open(funcfile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		desc[lst[0]] = [lst[0], lst[3]]

# fill in alias
with open(aliasfile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		if lst[2] in desc:
			desc[lst[2]][0] = lst[0]
		else:
			desc[lst[2]] = [lst[0], lst[1]]


# make symbol file
fout = open('AGPv2_5asymbol','w')
with open('AGPv2_5a.struct.txt') as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		# lst[10] is mrna name
		n = mrna2gene[lst[10]]
		if n in desc:
			fout.write('{0}\t{1}\t{2}\t{3}\n'.format(lst[10], desc[n][0], desc[n][1], lst[0]))
fout.close()

print '''

drop table if exists AGPv2_5asymbol;
create table AGPv2_5asymbol (
name varchar(255) not null,
symbol varchar(255) null,
description text null,
id int unsigned not null primary key,
index(name)
);
load data local infile 'AGPv2_5asymbol' into table AGPv2_5asymbol;
'''
