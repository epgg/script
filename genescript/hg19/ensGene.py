import sys
import os


if len(sys.argv) != 4:
	print 'Usage: {0} <ensGene.txt> <ensemblToGeneName.txt> <kgXref.txt>'.format(sys.argv[0])
	sys.exit()

infile, ens2symbolfile, kgxreffile = sys.argv[1:]

os.system('/home/xzhou/subtleKnife/script/refGene2bed {0} ensGene /home/xzhou/data/hg19/chromsize 1'.format(infile))


# load symbol - desc
s2d = {}
with open(kgxreffile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		if lst[4]!='' and lst[7]!='':
			s2d[lst[4]] = lst[7]



# load ensembl name - symbol - desc
desc = {}
with open(ens2symbolfile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		if lst[1] in s2d:
			desc[lst[0]] = (lst[1], s2d[lst[1]])
		else:
			desc[lst[0]] = (lst[1], 'No description')


fout = open('ensGenesymbol','w')
notfound = []
with open('ensGene.struct.txt') as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		if lst[10] in desc:
			fout.write('{0}\t{1}\t{2}\t{3}\n'.format(lst[10], desc[lst[10]][0], desc[lst[10]][1], lst[0]))
		else:
			notfound.append(lst[10])
fout.close()

if len(notfound) > 0:
	print '!!! {0} names in .struct.txt file not found in symbol file'.format(len(notfound))

print '''

drop table if exists ensGenesymbol;
create table ensGenesymbol (
name varchar(255) not null,
symbol varchar(255) null,
description text null,
id int unsigned not null primary key,
index(name)
);
load data local infile 'ensGenesymbol' into table ensGenesymbol;
'''
