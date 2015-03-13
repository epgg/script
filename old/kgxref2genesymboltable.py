import sys

if len(sys.argv) != 3:
	print 'Usage: {0} <kgXref.txt file> <temperary output file>'.format(sys.argv[0])
	sys.exit()


names = set()
dupnumber = 0
fout = open(sys.argv[2],'w')
with open(sys.argv[1]) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		if lst[4] == '':
			continue
		if lst[4] not in names:
			names.add(lst[4])
			fout.write('{0}\t{1}\n'.format(lst[4], 'no desc' if lst[7]=='' else lst[7]))
		else:
			dupnumber += 1
fout.close()

print '''drop table if exists geneSymbol;
create table geneSymbol (
  symbol varchar(40) not null primary key,
  description text null
);
load data local infile '{0}' into table geneSymbol;
'''.format(sys.argv[2])

if dupnumber > 0:
	print '{0} duplicated...'.format(dupnumber)
