import glob,sys,gzip,os

lst=glob.glob('*.fa.gz')


if len(lst)==0:
	sys.stderr.write('No *.fa.gz files found\n')
	sys.exit()

for f in lst:
	print '>'+(os.path.basename(f).split('.')[0])
	with gzip.GzipFile(f) as fin:
		fin.readline()
		for l in fin:
			print l.rstrip()
