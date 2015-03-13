import sys

if len(sys.argv)!=4:
	print '<bin file> <raw data> <output file>'
	sys.exit()


binfile, infile, outfile=sys.argv[1:]

bins ={}
with open(binfile) as fin:
	fin.readline()
	for line in fin:
		lst=line.rstrip().split('\t')
		bins[lst[0]]=['chr'+lst[1],int(lst[2]),int(lst[3])]

cc=1
fout=open('xx','w')
with open(infile) as fin:
	fin.readline()
	for line in fin:
		lst=line.rstrip().split('\t')
		if lst[3]=='0': continue
		m=bins[lst[0]]
		n=bins[lst[1]]
		fout.write('{0}\t{1}\t{2}\t{3}:{4}-{5},{6}\t{7}\t{8}\n'.format(
			m[0],m[1],m[2],
			n[0],n[1],n[2],lst[3],cc,
			'.' if m[0]!=n[0] else ('+' if m[1]<n[1] else '-')))
		cc+=1
		fout.write('{0}\t{1}\t{2}\t{3}:{4}-{5},{6}\t{7}\t{8}\n'.format(
			n[0],n[1],n[2],
			m[0],m[1],m[2],lst[3],cc,
			'.' if m[0]!=n[0] else ('+' if m[1]>n[1] else '-')))
		cc+=1
fout.close()

import os

os.system('sort -k1,1 -k2,2n xx > '+outfile)
os.unlink('xx')
os.system('bgzip '+outfile)
os.system('tabix -p bed '+outfile+'.gz')
