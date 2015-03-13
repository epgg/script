import sys

if len(sys.argv)!=3:
	print '<input pooled matrix> <output .gz base name>'
	sys.exit()

infile,outfile=sys.argv[1:]

def str2pos(ss):
	a=ss.split('|')[2]
	b=a.split(':')
	c=b[1].split('-')
	return [a, b[0], int(c[0]), int (c[1])]

fout=open(outfile,'w')
id=1

with open(infile) as fin:
	fin.readline()
	lst=fin.readline().strip().split('\t')
	bins=[str2pos(i) for i in lst]
	total=len(bins);
	for i in range(total):
		lst=fin.readline().rstrip().split('\t')
		c1=str2pos(lst[0])
		for j in range(1,len(lst)):
			if lst[j]=='NULL':
				continue
			if i==j-1:
				continue
			c2=bins[j-1]
			v=float(lst[j])
			fout.write('{0}\t{1}\t{2}\t{3},{4}\t{5}\t{6}\n'.format(c1[1],c1[2],c1[3],c2[0],v,id,'.' if c2[1]!=c1[1] else ('+' if c2[2]>c1[2] else '-')))
			id+=1
			fout.write('{0}\t{1}\t{2}\t{3},{4}\t{5}\t{6}\n'.format(c2[1],c2[2],c2[3],c1[0],v,id,'.' if c2[1]!=c1[1] else ('+' if c2[2]<c1[2] else '-')))
			id+=1
fout.close()

import os

os.system('sort -k1,1 -k2,2n {0} > xx'.format(outfile))
os.system('mv xx '+outfile)
os.system('bgzip '+outfile)
os.system('tabix -p bed '+outfile+'.gz')
