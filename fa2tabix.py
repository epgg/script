import sys,os

if len(sys.argv) != 3:
	print 'Usage: {0} <input fasta file> <basename of output tabix file>'.format(sys.argv[0])
	sys.exit()

step=1000

infile,outfile=sys.argv[1:]
fout=open(outfile,'w')
with open(infile) as fin:
	chrom=None
	offset=0
	seq=''
	for line in fin:
		line=line.rstrip()
		if line[0]=='>':
			s=line[1:]
			if s.startswith('lcl|'):
				s=s.split('|')[1].split()[0]
			if chrom is None:
				chrom=s
				offset=0
				seq=''
				continue
			fout.write('{0}\t{1}\t{2}\t{3}\n'.format(chrom,offset,offset+len(seq),seq))
			chrom=s
			offset=0
			seq=''
			continue
		if len(line)>0:
			i=0
			Seq=seq+line
			while i+step<len(Seq):
				fout.write('{0}\t{1}\t{2}\t{3}\n'.format(chrom,offset,offset+step,Seq[i:i+step]))
				offset=offset+step
				i=i+step
			seq=Seq[i:]
fin.close()

fout.write('{0}\t{1}\t{2}\t{3}\n'.format(chrom,offset,offset+len(seq),seq))
fout.close()

s='bgzip '+outfile
print s
os.system(s)
s='tabix -p bed '+outfile+'.gz'
print s
os.system(s)
