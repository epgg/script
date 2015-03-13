import sys
import os

infile='/home/xzhou/data/spombe201203/pombe_09052011.gff'

# load up gene structure
gene = {}
# key: mrna name like SPAC212.11
# val: [chr, strand, txstart, txstop, cdsstart, cdsstop, [exon starts], [exon stops] ]

with open(infile) as fin:
	for line in fin:
		lst = line.split('\t')
		start=int(lst[3])
		stop=int(lst[4])
		lst2=lst[8].split(' ; ')
		lst3=lst2[0].split()
		if lst3[0]!='mRNA': continue

		'''if lst[2] == 'mRNA':
			thismrna = lst[8].split(';')[0].split('=')[1]
			gene[thismrna] = [lst[0], lst[6], lst[3], lst[4], None, None, [], []]
		elif lst[2] == 'protein':
			gene[thismrna][4] = lst[3]
			gene[thismrna][5] = lst[4]
			'''
		if lst[2] == 'CDS':
			genename=lst3[1]
			if genename not in gene:
				gene[genename]=[lst[0], lst[6], None, None, None, None, [start], [stop]]
			else:
				gene[genename][6].append(start)
				gene[genename][7].append(stop)

# go over the file again to fill in txstart, txstop, cdsstart, cdsstop
# only use genes that CDS been recorded
# also grab alias, description
desc={}
with open(infile) as fin:
	for line in fin:
		lst=line.split('\t')
		if lst[2]=='mRNA':
			start=int(lst[3])
			stop=int(lst[4])
			lst2=lst[8].split(' ; ')
			lst3=lst2[0].split()
			if lst3[0]!='mRNA': continue
			genename=lst3[1]
			if genename in gene:
				gene[genename][2]=start
				gene[genename][3]=stop
				if lst[6]=='+':
					gene[genename][4]=min(gene[genename][6])
					gene[genename][5]=max(gene[genename][7])
				else:
					gene[genename][5]=min(gene[genename][6])
					gene[genename][4]=max(gene[genename][7])
				desc[genename]=[genename, 'no desc']
				for i in range(len(lst2)):
					lst3=lst2[i].split(' ',1)
					if lst3[0]=='Alias':
						desc[genename][0]=lst3[1].replace('"','')
					elif lst3[0]=='controlled_curation':
						arr=lst3[1].replace('"','').split(' ||| ')
						output=[]
						for i in range(len(arr)):
							tt=arr[i].split('; ')
							output.append('<table style=\'border-bottom:solid 1px #8F5Ab2;margin:5px;\'>')
							#output.append('<table>')
							for j in range(len(tt)):
								ss=tt[j].split('=')
								output.append('<tr><td valign=top style=\'font-style:italic;color:#D6B8ce\'>'+ss[0]+'</td><td style=\'color:#D6B8CE\'>'+ss[1]+'</td></tr>')
							output.append('</table>')
						desc[genename][1]=''.join(output)


# write that into gene structure table similar as ucsc's
fout = open('pombase_gene.txt','w')
for g in gene:
	# name, chrom, strand, txstart, txend, cdsstart, cdsend, exoncount, exonstarts, exonstops, 0, name2
	fout.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8},\t{9},\t0\t{0}\tcmpl\tcmpl\t{10},\n'.format(
		g, gene[g][0], gene[g][1], gene[g][2], gene[g][3], gene[g][4], gene[g][5], 
		len(gene[g][6]),
		','.join([str(n) for n in gene[g][6]]),
		','.join([str(n) for n in gene[g][7]]),
		','.join(['0' for i in range(len(gene[g][6]))])
		))
fout.close()


os.system('/home/xzhou/subtleKnife/script/refGene2bed pombase_gene.txt pombase_gene /home/xzhou/data/spombe201203/chrom.len 0')


fout = open('pombase_genesymbol','w')
with open('pombase_gene.struct.txt') as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		n = lst[10]
		if n in desc:
			fout.write('{0}\t{1}\t{2}\t{3}\n'.format(n, desc[n][0], desc[n][1], lst[0]))
fout.close()


print '''

drop table if exists pombase_genesymbol;
create table pombase_genesymbol (
name varchar(255) not null,
symbol varchar(255) null,
description text null,
id int unsigned not null primary key,
index(name)
);
load data local infile 'pombase_genesymbol' into table pombase_genesymbol;
'''
