import sys
import gzip

if len(sys.argv)!=3:
	print '<input file "ld_chr5_TSI.txt.gz"> <chrom> output to stdout'
	sys.exit()


c=sys.argv[2]
id=1
with gzip.GzipFile(sys.argv[1]) as fin:
	for line in fin:
		lst=line.rstrip().split()
		if len(lst)!=9:
			print line
			print 'wrong line'
			sys.exit()
		a=int(lst[0])
		b=int(lst[1])
		if a>b:
			print line
			print 'XXX'
			sys.exit()
		print '{0}\t{1[0]}\t{1[1]}\tid:{2},rs1:"{1[3]}",rs2:"{1[4]}",scorelst:[{1[5]},{1[6]},{1[7]},{1[8]}]'.format(c,lst,id)
		id+=1
