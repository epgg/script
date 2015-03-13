import sys

if len(sys.argv) != 3:
	print "require trackDb.ra file (integrative track or so-called container), and dummy letter at the end of track name"
	sys.exit()

with open(sys.argv[1]) as fin:
	tkname = ''
	label = ''
	for line in fin:
		line = line.strip()
		if line.startswith("track "):
			if line[-1] == sys.argv[2]:
				# track name
				tkname = line.split()[1][:-1]
		elif line.startswith("shortLabel"):
			label = line.split(' ',1)[1]
		elif line.startswith("metadata"):
			md = line.split(' ',1)[1]
			# geo
			lst = md.split(' ')[-1].split('=')
			geo = ''
			if len(lst)==2 and lst[0]=='GSM':
				geo = lst[1]
			else:
				sys.stderr.write(tkname+'\n')
			print '{0}\t{1}\t{2}\t{3}'.format(tkname, label, md, geo)
