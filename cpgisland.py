import sys,os

if len(sys.argv) != 3:
	print "Usage: {0} <cpgIslandExt.txt> <chr.size file>"
	sys.exit()


fout = open('cgitmp.bed','w')
i = 0
with open(sys.argv[1]) as fin:
	for line in fin:
		lst = line.split('\t')
		fout.write('{0[1]}\t{0[2]}\t{0[3]}\t.\t{1}\n'.format(lst, i))
		i+= 1
fout.close()


os.system("bedToBigBed cgitmp.bed {0} cpgisland.bigBed".format(sys.argv[2]))
