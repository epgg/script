import sys

if len(sys.argv)!=3:
	print '<input gff3> <gene track name>'
	sys.exit()

gff3,outfile=sys.argv[1:]

gene={}

def parse(s):
	h={}
	for a in s.split(';'):
		b=a.split('=')
		h[b[0]]=b[1]
	return h

with open(gff3) as fin:
	fin.readline()
	fin.readline()
	for line in fin:
		lst=line.rstrip().split('\t')
		h=parse(lst[8])
		if lst[2]=='mRNA':
			gene[h['pacid']]=[lst[0],lst[3],lst[4],lst[6],[],[],h['Name']]
		elif lst[2]=='five_prime_UTR' or lst[2]=='three_prime_UTR':
			if h['pacid'] in gene:
				gene[h['pacid']][4].append([lst[3],lst[4]])
		elif lst[2]=='CDS':
			if h['pacid'] in gene:
				gene[h['pacid']][5].append([lst[3],lst[4]])

fout=open(outfile,'w')
fout2=open(outfile+'names','w')
for n in gene:
	g=gene[n]
	fout2.write('{0}\t{1}\t{2}\t{3}\n'.format(g[0],g[1],g[2],g[6]))
	fout.write('{0}\t{1}\t{2}\tname:"{3}",strand:"{4}",struct:{{'.format(g[0],g[1],g[2],g[6],g[3]))
	if len(g[4])>0:
		fout.write('thin:[')
		for v in g[4]:
			fout.write('[{0},{1}],'.format(v[0],v[1]))
		fout.write('],')
	if len(g[5])>0:
		fout.write('thick:[')
		for v in g[5]:
			fout.write('[{0},{1}],'.format(v[0],v[1]))
		fout.write('],')
	fout.write('}\n')
fout.close()
fout2.close()

import os
os.system('sort -k1,1 -k2,2n '+outfile+' > x')
os.system('mv x '+outfile)
os.system('bgzip '+outfile)
os.system('tabix -p bed '+outfile+'.gz')


print '''

drop table if exists {0};
create table {0}(
chrom varchar(20) not null,
start int unsigned not null,
stop int unsigned not null,
name varchar(100) not null
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
load data local infile '{0}names' into table {0};
create index name on {0} (name);
'''.format(outfile)

