import sys, os


if len(sys.argv) != 5:
	print 'require: <ucsc bed12 file> <0/1 to omit first line? ><chromsize file> <output file basename>'
	sys.exit()

infile, no1, chrsizefile, outfile = sys.argv[1:]

no1 = no1=='1'

fout = open(outfile, 'w')

ii = 1
with open(infile) as fin:
	if no1:
		fin.readline()
	for line in fin:
		lst = line.rstrip().split('\t')
		start = int(lst[1])
		stop = int(lst[2])
		tt = lst[10].split(',')
		w1 = int(tt[0])
		w2 = int(tt[1])
		fout.write('{0}\t{1}\t{2}\t{0}:{3}-{4},{7}\t{5}\t+\n{0}\t{3}\t{4}\t{0}:{1}-{2},{7}\t{6}\t-\n'.format(
			lst[0], # 0
			start,start+w1, # 1,2
			stop-w2,stop, # 3,4
			ii,ii+1, # 5,6
			lst[4])) # 7
		ii += 2
fout.close()


os.system('bedSort {0} {0}'.format(outfile))
os.system('bedToBigBed {0} {1} {0}.bigBed'.format(outfile, chrsizefile))

