import sys
import os


if len(sys.argv) != 3:
	print 'Usage: {0} <knownGene.txt> <kgXref.txt>'.format(sys.argv[0])
	sys.exit()

knowngenefile, kgxreffile = sys.argv[1:]

os.system('/home/xzhou/subtleKnife/script/refGene2bed {0} knownGene /home/xzhou/data/hg19/chromsize 0'.format(knowngenefile))


# load name - symbol - desc
desc = {}
with open(kgxreffile) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		if lst[0]!='' and lst[4]!='' and lst[7]!='':
			desc[lst[0]] = (lst[4], lst[7])




fout = open('knownGenesymbol','w')
notfound = []
with open('knownGene.struct.txt') as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		if lst[10] in desc:
			fout.write('{0}\t{1}\t{2}\t{3}\n'.format(lst[10], desc[lst[10]][0], desc[lst[10]][1], lst[0]))
		else:
			notfound.append(lst[10])
fout.close()

if len(notfound) > 0:
	print '!!! name in .struct.txt file not found in symbol file:',', '.join(notfound)

print '''

drop table if exists knownGenesymbol;
create table knownGenesymbol (
name varchar(255) not null,
symbol varchar(255) null,
description text null,
id int unsigned not null primary key,
index(name)
);
load data local infile 'knownGenesymbol' into table knownGenesymbol;
'''

