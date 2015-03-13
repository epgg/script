import sys

if len(sys.argv) != 2:
	print "require rmsk.txt file, output to one file per each class\nTo get class, run cut -f12 rmsk.txt|sort -u"
	sys.exit()



classes = ['SINE', 'LINE', 'LTR', 'DNA', 'Simple_repeat', 'Low_complexity', 'Satellite', 'RNA', 'Other', 'Unknown']

fout = {}
for c in classes:
	fout[c] = [open(c+'.bed', "w"), 0]

with open(sys.argv[1]) as fin:
	for line in fin:
		lst = line.split('\t')
		for c,f in fout.items():
			if c in lst[11]:
				f[0].write('{0[5]}\t{0[6]}\t{0[7]}\t{0[9]}\t{0[10]}\t{1}\n'.format(lst, f[1]))
				f[1] += 1
				break

for f in fout.values():
	f[0].close()
