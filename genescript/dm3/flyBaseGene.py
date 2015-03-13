import sys
import os


if len(sys.argv) != 3:
	print 'Usage: {0} <flyBaseGene.txt> <flyBaseToDescription.txt>'.format(sys.argv[0])
	sys.exit()

infile, todescfile = sys.argv[1:]

os.system('/home/xzhou/subtleKnife/script/refGene2bed {0} flyBaseGene /home/xzhou/data/dm3/chromsize 1'.format(infile))


# load name - desc
n2d = {}
with open(todescfile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		n2d[lst[0]] = lst[1]



fout = open('flyBaseGenesymbol','w')
with open('flyBaseGene.struct.txt') as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		fout.write('{0}\t{0}\t{1}\t{2}\n'.format(lst[10], n2d[lst[10]] if lst[10] in n2d else 'No description', lst[0]))
fout.close()

print '''

drop table if exists flyBaseGenesymbol;
create table flyBaseGenesymbol (
name varchar(255) not null,
symbol varchar(255) null,
description text null,
id int unsigned not null primary key,
index(name)
);
load data local infile 'flyBaseGenesymbol' into table flyBaseGenesymbol;
'''
