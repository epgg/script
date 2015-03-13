import sys


if len(sys.argv) != 2:
	print "require trackDetail file (3rd column is ucsc metadata line"
	sys.exit()


# from: molecule="genomic DNA"
# convert to: molecule=genomic DNA;

# from: <a href="xx">yyy</a>
# convert to: yyy


with open(sys.argv[1]) as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		md = lst[2]
		while '<a href=' in md:
			a,b = md.split('<a href=', 1)
			c,d = b.split('>', 1)
			e,f = d.split('</a>',1)
			md = a+e+f
		if ';' in md:
			print '; still exists in line '+line
			sys.exit()
		md = md.replace('"','')
		arr = md.split('=')
		new = arr[0]
		for x in arr[1:-1]:
			lst2 = x.split(' ')
			new += '='+' '.join(lst2[:-1])+'; '+lst2[-1]
		new += '='+arr[-1]
		
		if 0:
			for x in new.split('; '):
				print x
		print '{0}\t{1}\t{2}\t{3}'.format(lst[0], lst[1], new, lst[3])
