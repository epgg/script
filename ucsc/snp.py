import sys

if len(sys.argv)!=4:
	print '<input UCSC SNP .txt file> <output lookup file> <output tk file>'
	sys.exit()

id_chr=1
id_start=2
id_stop=3
id_name=4
id_strand=6
id_refseq=7
id_observeseq=9
id_class=11
id_validation=12
id_avhet=13
id_avhetstd=14
id_function=15
id_allelefreqcount=21
id_alleles=22
id_allelefreq=24

# class identifiers to go into track item json, can be any unique string
class2id={'single':1,
'in-del':2,
'het':3,
'microsatellite':4,
'named':5,
'mixed':6,
'mnp':7,
'insertion':8,
'deletion':9}

fout=open(sys.argv[2],'w')
fout2=open(sys.argv[3],'w')

id=1
skip=0
with open(sys.argv[1]) as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		if lst[id_class] not in class2id:
			skip+=1
			continue
		fout.write('{0}\t{1}\t{2}\t{3}\n'.format(lst[id_chr],lst[id_start],lst[id_stop],lst[id_name]))
		fout2.write('{0}\t{1}\t{2}\tid:{3},name:"{4}",strand:"{5}",category:{6},details:{{refNCBI:"{7}",observed:"{8}"'.format(
			lst[id_chr],
			lst[id_start],
			lst[id_stop],
			id,
			lst[id_name],
			lst[id_strand],
			class2id[lst[id_class]],
			lst[id_refseq],
			lst[id_observeseq]))
		if lst[id_validation]!='':
			fout2.write(',validation:"'+lst[id_validation]+'"')
		if lst[id_avhet]!='':
			fout2.write(',"average heterozygosity":"'+lst[id_avhet]+', std:'+lst[id_avhetstd]+'"')
		if lst[id_function]!='':
			fout2.write(',function:"'+lst[id_function]+'"')
		if int(lst[id_allelefreqcount])>0:
			fout2.write(',alleles:"{0}","allele frequencies":"{1}"'.format(lst[id_alleles],lst[id_allelefreq]))
		fout2.write('}\n')

		id+=1
fout.close()
fout2.close()

import os
os.system('bgzip '+sys.argv[3])
os.system('tabix -p bed '+sys.argv[3]+'.gz')

print '''
drop table if exists snp;
create table snp (
  chrom varchar(20) not null,
  start int unsigned not null,
  stop int unsigned not null,
  name varchar(100) not null primary key
);
load data local infile '{0}' into snp;
\n\nskipped {1} items
'''.format(sys.argv[2],skip)
