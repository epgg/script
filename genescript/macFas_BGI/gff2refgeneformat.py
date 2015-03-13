import sys

if len(sys.argv)!=2:
	print '<input gff> output to stdout'
	sys.exit()



gene={}
'''
mrna id : {
	chr
	strand
	start
	stop
	cdsstarts : []
	cdsstops : []
	attr : {}
}
'''

def eat(s):
	a={}
	for ss in s.split(';'):
		t=ss.split('=')
		if len(t)==2:
			a[t[0]]=t[1]
	return a

with open(sys.argv[1]) as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		if not lst[0].startswith('chr'): continue
		h=eat(lst[8])
		if lst[2]=='mRNA':
			if 'ID' in h:
				thisgene={'chr':lst[0],'start':lst[3],'stop':lst[4],'strand':lst[6],'cdsstarts':[],'cdsstops':[],'attr':{'program':lst[1]}}
				if 'alignRate' in h:
					thisgene['align rate']=h['alignRate']
				if 'identity' in h:
					thisgene['identity']=h['identity']
				gene[h['ID']]=thisgene
		elif lst[2]=='CDS':
			gene[h['Parent']]['cdsstarts'].append(int(lst[3]))
			gene[h['Parent']]['cdsstops'].append(int(lst[4]))
		else:
			raise Exception('unknown type '+lst[2]);

for id in gene:
	c1=sorted(gene[id]['cdsstarts'])
	c2=sorted(gene[id]['cdsstops'])
	print '1\t{0}\t{1[chr]}\t{1[strand]}\t{1[start]}\t{1[stop]}\t{2}\t{3}\t{4}\t{5},\t{6},\t0\t'.format(
		id,
		gene[id],
		min(c1),
		max(c2),
		len(c1),
		','.join([str(x) for x in c1]),
		','.join([str(x) for x in c2])
		)
