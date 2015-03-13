import sys,gzip

if len(sys.argv)!=3:
	print '<kegg2ncbi, get by "http://rest.kegg.jp/conv/??/ncbi-geneid"> <tax id> output to stdout'
	sys.exit()



ncbi2kegg={}
with open(sys.argv[1]) as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		ncbi2kegg[lst[0].split(':')[1]] = lst[1].split(':')[1]


result={}
with gzip.GzipFile('/home/xzhou/data/gene2refseq.gz') as fin:
	fin.readline()
	for line in fin:
		lst=line.rstrip().split('\t')
		if lst[0]==sys.argv[2]:
			if lst[1] in ncbi2kegg:
				if len(lst[3])>0:
					result[ncbi2kegg[lst[1]]] = lst[3].split('.')[0]

for k in result:
	print '{0}\t{1}'.format(k,result[k])
