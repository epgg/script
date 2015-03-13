import sys

lst=[]
with open(sys.argv[1]) as fin:
	for line in fin:
		lst.append(line.split('\t')[0])
print ','.join(lst)
