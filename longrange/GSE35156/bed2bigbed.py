import sys,glob,os


if len(sys.argv) != 3:
	print '<input directory of bed files (basename.bed), must with backslash> <chr size file> output to same directory'
	sys.exit()



indir, chrsizefile = sys.argv[1:]

flst = glob.glob(indir+'*.bed')

for f in flst:
	os.system('/home/comp/twlab/xzhou/bin/x86_64/bedToBigBed {0} {1} {2}.bigBed'.format(f,chrsizefile,f.split('.')[0]))
