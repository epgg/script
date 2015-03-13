import sys
import os

if len(sys.argv) != 2:
	print '''Usage: {0} <UCSC rmsk.txt> output to current dir
	one track for each class and family'''.format(sys.argv[0])
	sys.exit()


rmsk = sys.argv[1]

fout = {}

classes={}
f2c={} # key: f, val: c

print 'surveying family-to-class...'
with open(sys.argv[1]) as fin:
	for line in fin:
		lst = line.split('\t')
		c=lst[11]
		f=lst[12]
		classes[c]=1
		f2c[f]=c


fout=open('decorInfo','w')
fout2=open('track2Detail','w')
fout3=open('track2Style','w')

date='March 8, 2014'
source='http://hgdownload.soe.ucsc.edu/goldenPath/cavPor3/database/'

for c in classes:
	fout.write('{0}\t{0}\t\N\t4\t24\t0\t\N\n'.format(c))
	fout2.write('{0}\tdownload_date={1}; source={2}\n'.format(c,date,source))
	fout3.write(c+'\tshowscoreidx:1,scorenamelst:["Smith-Waterman score","SW score normalized by length"]\n')

for f in f2c:
	c=f2c[f]
	fout.write('{1}{0}\t{0} ({1})\t{1}\t4\t24\t0\t\N\n'.format(f,c))
	fout2.write('{1}{0}\tdownload_date={2}; source={3}\n'.format(f,c,date,source))
	fout3.write(c+f+'\tshowscoreidx:1,scorenamelst:["Smith-Waterman score","SW score normalized by length"]\n')

fout.close()
fout2.close()
fout3.close()

print str(len(f2c.keys()))+' families, from '+str(len(classes.keys()))+' classes'
for k in f2c:
	print '{0}\t-->\t{1}'.format(k,f2c[k])
print



foutc = {}
for c in classes:
	foutc[c] = [open(c+'.bed','w'), 1, c]
fout = {}
for f in f2c:
	fout[f] = [open(f2c[f]+f+'.bed','w'), 1, f2c[f]+f]
print 'generating bed files...'
skip2 = 0
with open(sys.argv[1]) as fin:
	for line in fin:
		lst = line.split('\t')
		classname = lst[11]
		if lst[12] in f2c and classname in classes:
			string='{0[5]}\t{0[6]}\t{0[7]}\tname:"{0[10]}",strand:"{0[9]}",scorelst:[{0[1]},{3}],details:{{Divergence:"{4}%",Deletion:"{5}%",Insertion:"{6}%","Repbase class":"{1}","Repbase family":"{2}"}}'.format(
				lst,classname,lst[12],
				int(lst[1])/(int(lst[7])-int(lst[6])),
				int(lst[2])/10,
				int(lst[3])/10,
				int(lst[4])/10
				)
			# this family
			fout[lst[12]][0].write('{0},id:{1}\n'.format(string, fout[lst[12]][1]))
			fout[lst[12]][1] += 1
			# its class
			foutc[classname][0].write('{0},id:{1}\n'.format(string, foutc[classname][1]))
			foutc[classname][1] += 1
		else:
			skip2 += 1

for f in fout:
	fout[f][0].close()
	cmd='sort -k1,1 -k2,2n {0}.bed > {0}'.format(fout[f][2])
	print cmd
	os.system(cmd)
	cmd='bgzip '+fout[f][2]
	print cmd
	os.system(cmd)
	cmd='tabix -p bed '+fout[f][2]+'.gz'
	print cmd
	os.system(cmd)
for f in foutc:
	foutc[f][0].close()
	cmd = 'sort -k1,1 -k2,2n {0}.bed > {0}'.format(foutc[f][2])
	print cmd
	os.system(cmd)
	cmd = 'bgzip '+foutc[f][2]
	print cmd
	os.system(cmd)
	cmd='tabix -p bed '+foutc[f][2]+'.gz'
	print cmd
	os.system(cmd)
if skip2 > 0:
	print '{0} homeless items writen to file "skip.bed"'.format(skip2)
