import sys
import os


if len(sys.argv) != 3:
	print 'Usage: {0} <ensGene.txt> <ensemblToGeneName.txt>'.format(sys.argv[0])
	sys.exit()

infile, namefile = sys.argv[1:]

os.system('/home/xzhou/subtleKnife/script/refGene2bed {0} ensGene /home/xzhou/data/dm3/chromsize 1'.format(infile))


# load name - symbol
n2s = {}
with open(namefile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		n2s[lst[0]] = lst[1]



fout = open('ensGenesymbol','w')
with open('ensGene.struct.txt') as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		fout.write('{0}\t{1}\tNo description\t{2}\n'.format(lst[10], n2s[lst[10]] if lst[10] in n2s else lst[10], lst[0]))
fout.close()

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
