import sys,gzip
sys.path.append('/srv/epgg/data/subtleKnife/script/genescript')
import parseUcscgenestruct

def xopen(f,mode='rb'):
    return gzip.open(f,mode)

tkname='gencodeV19'


cateinfo={'coding':1,
	'nonCoding':2,
	'pseudo':3,
	'problem':4,
	}



genes={}
# actually transcripts
# key: transcript id, val: raw lst
with xopen('wgEncodeGencodeCompV19.txt.gz') as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		genes[lst[1]]=lst
with xopen('wgEncodeGencodePseudoGeneV19.txt.gz') as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		if lst[1] in genes:
			print 'Overriding '+lst[1]
		genes[lst[1]]=lst
with xopen('wgEncodeGencode2wayConsPseudoV19.txt.gz') as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		if lst[1] in genes:
			print 'Overriding '+lst[1]
		genes[lst[1]]=lst



remark={}
# key: transcript id
with xopen('wgEncodeGencodeAnnotationRemarkV19.txt.gz') as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		if len(lst)<2: continue
		remark[lst[0]]=lst[1].replace('"','')


uniprot={}
with xopen('wgEncodeGencodeUniProtV19.txt.gz') as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		if lst[0] not in uniprot:
			uniprot[lst[0]]=[]
		uniprot[lst[0]].append(lst[1])



pubmed={}
with xopen('wgEncodeGencodePubMedV19.txt.gz') as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		if lst[0] not in pubmed:
			pubmed[lst[0]]=[]
		pubmed[lst[0]].append(lst[1])



refseq={}
with xopen('wgEncodeGencodeRefSeqV19.txt.gz') as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		refseq[lst[0]]=[lst[1]]
		if len(lst)==3:
			refseq[lst[0]].append(lst[2])


desc={}
with xopen('kgXref.txt.gz') as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		if len(lst)>=8 and len(lst[7])>0:
			w=lst[7].replace('"','')
			if len(lst[5])>0:
				desc[lst[5]]=w
			if len(lst[6])>0:
				desc[lst[6]]=w
			if len(lst[4])>0:
				desc[lst[4]]=w




# dump
fout=open(tkname,'w')
fout2=open(tkname+'_load','w')

id=1

with xopen('wgEncodeGencodeAttrsV19.txt.gz') as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		transcript=lst[4]
		if transcript not in genes: continue
		g=parseUcscgenestruct.parse(genes[transcript],True)
		fout.write('{0}\t{1}\t{2}\tname:"{3}",id:{4},strand:"{5}",'.format(
			g['chrom'],
			g['start'],
			g['stop'],
			lst[1] if len(lst[1])>0 else transcript,
			id,
			g['strand']))
		id+=1
		if 'thin' in g or 'thick' in g:
			fout.write('struct:{')
			if 'thin' in g:
				fout.write('thin:[')
				for x in g['thin']:
					fout.write('[{0},{1}],'.format(x[0],x[1]))
				fout.write('],')
			if 'thick' in g:
				fout.write('thick:[')
				for x in g['thick']:
					fout.write('[{0},{1}],'.format(x[0],x[1]))
				fout.write('],')
			fout.write('},')

		# category
		fout.write('category:'+str(cateinfo[lst[12]])+',')

		# desc
		flag=True
		if transcript in refseq:
			n=refseq[transcript][0].split('.')[0]
			if n in desc:
				fout.write('desc:"'+desc[n]+'",')
				flag=False
			else:
				if len(refseq[transcript])==2:
					n=refseq[transcript][1].split('.')[0]
					if n in desc:
						fout.write('desc:"'+desc[n]+'",')
						flag=False
		if flag and lst[1] in desc:
			fout.write('desc:"'+desc[lst[1]]+'",')

		fout.write('details:{')

		fout.write('"Gene ID":"<a href=http://www.ensembl.org/Homo_sapiens/Gene/Summary?db=core;t={0} class=w target=_blank>{0}</a>",'.format(lst[0]))
		fout.write('"Transcript ID":"<a href=http://www.ensembl.org/Homo_sapiens/Transcript/Summary?db=core;t={0} class=w target=_blank>{0}</a>",'.format(transcript))

		if transcript in remark:
			fout.write('Remark:"'+remark[transcript]+'",')
		if transcript in uniprot:
			fout.write('UniProt:"'+('<br>'.join(['<a href=http://www.uniprot.org/uniprot/'+x+' class=w target=_blank>'+x+'</a>' for x in uniprot[transcript]]))+'",')
		if transcript in pubmed:
			fout.write('PubMed:"'+('<br>'.join(['<a href=http://www.ncbi.nlm.nih.gov/pubmed/'+x+' class=w target=_blank>'+x+'</a>' for x in pubmed[transcript]]))+'",')
		if transcript in refseq:
			n=refseq[transcript][0]
			fout.write('RefSeq:"<a href=http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Search&db=Nucleotide&doptcmdl=GenBank&term='+n+' class=w target=_blank>'+n+'</a>')
			if len(refseq[transcript])==2:
				n=refseq[transcript][1]
				fout.write(', <a href=http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Search&db=Nucleotide&doptcmdl=GenBank&term='+n+' class=w target=_blank>'+n+'</a>')
			fout.write('",');

		if len(lst[2])>0:
			fout.write('"Gene bioType":"<a href=http://www.gencodegenes.org/gencode_biotypes.html class=w target=_blank>'+lst[2]+'</a>",')
		if len(lst[6])>0:
			fout.write('"Transcript bioType":"<a href=http://www.gencodegenes.org/gencode_biotypes.html class=w target=_blank>'+lst[6]+'</a>",')

		fout.write('}')
		# end of details

		fout.write('\n')

		fout2.write('{0}\t{1}\t{2}\t{3}\n'.format(g['chrom'],g['start'],g['stop'],lst[0]))
		fout2.write('{0}\t{1}\t{2}\t{3}\n'.format(g['chrom'],g['start'],g['stop'],lst[1]))
		fout2.write('{0}\t{1}\t{2}\t{3}\n'.format(g['chrom'],g['start'],g['stop'],lst[4]))


fout2.close()


# add polyA regions
with xopen('wgEncodeGencodePolyaV19.txt.gz') as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		fout.write('{0}\t{1}\t{2}\tcategory:5,strand:"{3}",id:{4}\n'.format(lst[2],lst[4],lst[5],lst[3],id))
		id+=1

fout.close()

import os
os.system('sort -k1,1 -k2,2n '+tkname+' > x')
os.system('mv x '+tkname)
os.system('bgzip '+tkname)
os.system('tabix -p bed '+tkname+'.gz')

print '''
drop table if exists {0};
create table {0} (
chrom varchar(20) not null,
start int unsigned not null,
stop int unsigned not null,
name varchar(100) not null
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
load data local infile '{0}_load' into table {0};
create index name on {0} (name);
'''.format(tkname)

print "cateInfo:{1:['coding','rgb(0,60,179)'], 2:['non-coding','rgb(0,128,0)'], 3:['pseudogene','rgb(230,0,172)'], 4:['problem','rgb(255,0,0)'], 5:['polyA','rgb(0,0,51)']},dbsearch:true"
