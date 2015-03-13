import sys
import os

if len(sys.argv) != 3:
	print 'Usage: {0} <ZmB73_5a_xref.txt> <AGPv2_5a.txt (generated by b73_5a.py)> output to current dir'.format(sys.argv[0])
	sys.exit()


xreffile, allfile = sys.argv[1:]


gn2refgene = {} # gene name : refgene name
desc = {} # refgene name : desc

with open(xreffile) as fin:
	fin.readline()
	for line in fin:
		lst = line.rstrip().split('\t')
		if lst[1].startswith('RefSeq_'):
			gn2refgene[lst[0]] = lst[2]
			desc[lst[2]] = lst[3]


fout = open('refgene.txt', 'w')
with open(allfile) as fin:
	for line in fin:
		lst = line.split('\t')
		if lst[0] in gn2refgene:
			fout.write('{0}\t{1[1]}\t{1[2]}\t{1[3]}\t{1[4]}\t{1[5]}\t{1[6]}\t{1[7]}\t{1[8]}\t{1[9]}\t{1[10]}\t{0}\t{1[12]}\t{1[13]}\t{1[14]}'.format(gn2refgene[lst[0]], lst))
fout.close()


os.system('/home/xzhou/subtleKnife/script/refGene2bed refgene.txt refGene /home/xzhou/data/b73_AGPv2/chromsize 0')

fout = open('refGenesymbol', 'w')
with open('refGene.struct.txt') as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		fout.write('{0}\t{0}\t{1}\t{2}\n'.format(lst[10], desc[lst[10]], lst[0]))
fout.close()

print '''

drop table if exists refGenesymbol;
create table refGenesymbol (
name varchar(255) not null,
symbol varchar(255) null,
description text null,
id int unsigned not null primary key,
index(name)
);
load data local infile 'refGenesymbol' into table refGenesymbol;
'''
