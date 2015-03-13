# using wouter's awesome matrix for chromhmm

import sys

if len(sys.argv)!=3:
	print '<input matrix> <output file name>'
	sys.exit()

infile,outfile=sys.argv[1:]

fout=open(outfile,'w')
layercount=0
lineid=0
iid=1
with open(infile) as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		if layercount==0:
			layercount=len(lst)-3
		elif layercount!=len(lst)-3:
			print 'Wrong layer count at line '+str(lineid)
			sys.exit()
		lineid+=1
		fout.write('{0}\t{1}\t{2}\tlayers:[{3}],id:{4}\n'.format(lst[0],lst[1],lst[2],','.join(lst[3:]),iid))
		iid+=1
fout.close()

print str(layercount)+' layers'
import os
os.system('sort -k1,1 -k2,2n '+outfile+' > tmpfile')
os.system('mv tmpfile '+outfile)
os.system('bgzip '+outfile)
os.system('tabix -p bed '+outfile+'.gz')
