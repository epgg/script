
import sys

if len(sys.argv)!=3:
	print '<input geo file> <output .gz file base name>'
	sys.exit()

outfile=sys.argv[2]
fout=open(outfile,'w')
cc=1
with open(sys.argv[1]) as fin:
	for line in fin:
		if line[0]=='#': continue
		lst=line.rstrip().split('\t')
		if len(lst)!=4: continue
		c1=lst[0].split('|')[2]
		c2=c1.split(':')
		c3=c2[1].split('-')
		cp=int(c3[0])
		m1=lst[1].split('|')[2]
		m2=m1.split(':')
		m3=m2[1].split('-')
		mp=int(m3[0])
		fout.write('{0}\t{1}\t{2}\t{3},{4}\t{5}\t{6}\n'.format(
			c2[0],
			c3[0], c3[1],
			m1,
			lst[2],
			cc,
			'.' if c2[0]!=m2[0] else ('+' if mp>cp else '-')))
		cc+=1
		fout.write('{0}\t{1}\t{2}\t{3},{4}\t{5}\t{6}\n'.format(
			m2[0],
			m3[0], m3[1],
			c1,
			lst[2],
			cc,
			'.' if c2[0]!=m2[0] else ('+' if cp>mp else '-')))
		cc+=1
fout.close()

import os

os.system('sort -k1,1 -k2,2n '+outfile+' > xx')
os.system('mv xx '+outfile)
os.system('bgzip '+outfile)
os.system('tabix -p bed '+outfile+'.gz')
