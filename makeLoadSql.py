import sys
import os.path
import glob

ofn = 'load.sql'

# GF bed
datadir = '/home/xzhou/data/hg19/bed'
if os.path.exists(os.path.join(datadir, ofn)):
	os.unlink(os.path.join(datadir, ofn))
fout = open(os.path.join(datadir, ofn), 'w')
for f in glob.glob(os.path.join(datadir, '*')):
	tn = os.path.basename(f).split('.')[0] + 'Bed'
	fout.write('''
drop table if exists `{0}`;
create table `{0}` (
  chrom char(20) not null,
  start int not null,
  stop int not null,
  strand char(1) null,
  name varchar(255) null,
  id int not null primary key
);
load data local infile '{1}' into table `{0}`;\n'''.format(tn, f))

# GF covering
datadir = '/home/xzhou/data/hg19/covering'
if os.path.exists(os.path.join(datadir, ofn)):
	os.unlink(os.path.join(datadir, ofn))
fout = open(os.path.join(datadir, ofn), 'w')
for f in glob.glob(os.path.join(datadir, '*')):
	tn = os.path.basename(f).split('.')[0] + 'Covering'
	fout.write('''
drop table if exists `{0}`;
create table `{0}` (
  id int not null,
  chrom char(20) not null,
  start int not null,
  stop int not null,
  itemNumber int not null,
  coordString text not null,
  primary key (id),
  index(chrom, start),
  index(chrom, stop)
);
load data local infile '{1}' into table `{0}`;\n'''.format(tn, f))


