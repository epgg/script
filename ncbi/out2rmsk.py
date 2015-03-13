import gzip,os,glob


lst=glob.glob('*.rm.out.gz')
if len(lst)==0:
	raise Exception('No .rm.out.gz files found\n')

'''
1 `bin` smallint(5) unsigned NOT NULL,
2 `swScore` int(10) unsigned NOT NULL,
3 `milliDiv` int(10) unsigned NOT NULL,
4 `milliDel` int(10) unsigned NOT NULL,
5 `milliIns` int(10) unsigned NOT NULL,
6 `genoName` varchar(255) NOT NULL,
7 `genoStart` int(10) unsigned NOT NULL,
8 `genoEnd` int(10) unsigned NOT NULL,
9 `genoLeft` int(11) NOT NULL,
10`strand` char(1) NOT NULL,
11`repName` varchar(255) NOT NULL,
12`repClass` varchar(255) NOT NULL,
13`repFamily` varchar(255) NOT NULL,
14`repStart` int(11) NOT NULL,
15`repEnd` int(11) NOT NULL,
16`repLeft` int(11) NOT NULL,
17`id` char(1) NOT NULL,
'''


for f in lst:
	chr=os.path.basename(f).split('.')[0]
	with gzip.GzipFile(f) as fin:
		fin.readline()
		fin.readline()
		fin.readline()
		for l in fin:
			lst=l.strip().split()
			tmp=lst[10].split('/')
			cls=tmp[0]
			fam=cls if len(tmp)==1 else tmp[1]
			print '1\t{0[0]}\t{1}\t{2}\t{3}\t{4}\t{0[5]}\t{0[6]}\t\t{5}\t{0[9]}\t{6}\t{7}\t'.format(
				lst,
				int(float(lst[1])*10),
				int(float(lst[2])*10),
				int(float(lst[3])*10),
				chr,
				'-' if lst[8]=='C' else '+',
				cls,
				fam,
				)
