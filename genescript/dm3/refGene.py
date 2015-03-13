import sys
import os


if len(sys.argv) != 2:
	print 'Usage: {0} <refGene.txt>'.format(sys.argv[0])
	sys.exit()

infile = sys.argv[1]

os.system('/home/xzhou/subtleKnife/script/refGene2bed {0} refGene /home/xzhou/data/dm3/chromsize 1'.format(infile))


# load name - symbol
n2s = {}
with open(infile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		n2s[lst[1]] = lst[12]



fout = open('refGenesymbol','w')
with open('refGene.struct.txt') as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		fout.write('{0}\t{1}\tNo description\t{2}\n'.format(lst[10], n2s[lst[10]] if lst[10] in n2s else lst[10], lst[0]))
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
