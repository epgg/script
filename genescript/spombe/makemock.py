import sys
import os.path

'''
if len(sys.argv) == 1:
	print 'require chromosome length file'
	sys.exit()

start = 21000000
clen = 62500
chrom = "chr10"
'''

indir = '/home/xzhou/subtleKnife/mock'

chrom = 'chromosome3'
start = 322645
clen = 400
fileid = 1

with open(os.path.join(indir, "scaf")) as scaf:
	for line in scaf:
		lst = line.rstrip().split('\t')
		bn = "mock"+str(fileid)
		fout = open(bn,'w')
		for i in range(len(lst)):
			if(lst[i] != ''):
				fout.write("{0}\t{1}\t{2}\t{3}\n".format(chrom, start+i*clen, start+(i+1)*clen, lst[i]))
		fout.close()
		#os.system("bedGraphToBigWig {0} {1} {0}.bigWig".format(bn, sys.argv[1]))
		os.system('bgzip '+bn)
		os.system('tabix -p bed '+bn+'.gz')
		fileid += 1
