import sys


if len(sys.argv) != 2:
	print "require file cytoBandIdeo.txt"
	sys.exit()

# hg19 mm9

conv = {'acen':-1,
'gneg':0,
'gpos25':1,
'gpos25':1,
'gpos50':2,
'gpos75':3,
'gpos100':4,
'gvar':5,
'stalk':6,
'gpos33':7,
'gpos66':8,
'gneg':0,
'gpos':2,
'gvar':5}


with open(sys.argv[1]) as fin:
	while 1:
		line = fin.readline()
		if line == '': break
		lst = line.rstrip().split('\t')
		if lst[4] == 'acen':
			print '\t{0[0]}\t{0[1]}\t{0[2]}\t{0[3]}\t-1'.format(lst)
			lst = fin.readline().split('\t')
			print '\t{0[0]}\t{0[1]}\t{0[2]}\t{0[3]}\t-2'.format(lst)
			continue
		if lst[4] not in conv:
			print '{0} not found'.format(lst[4])
			sys.exit()
		print '\t{0[0]}\t{0[1]}\t{0[2]}\t{0[3]}\t{1}'.format(lst,conv[lst[4]])

sys.stderr.write('''
drop table if exists cytoband;
create table cytoband (
  id int unsigned not null primary key auto_increment,
  chrom char(10) not null,
  start int not null,
  stop int not null,
  name char(20) not null,
  colorIdx tinyint not null
);
load data local infile "cytoband" into table cytoband;
''')
