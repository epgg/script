import sys
import os.path


if len(sys.argv) != 3:
	print 'require tabular file with track name at first column, and bigWig file dir'
	sys.exit()



attrFile, bbdir = sys.argv[1:]


allarethere = True
with open(attrFile) as fin:
	for line in fin:
		lst = line.split('\t')
		f = os.path.join(bbdir, lst[0]+'.bigWig')
		if not os.path.exists(f):
			print f+' wrong'
			allarethere = False
		try:
			os.stat(f)
		except:
			print f+' wrong'
			allarethere = False

if allarethere:
	print "All bigwig track files in place."
