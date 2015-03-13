import sys
import os


if len(sys.argv) != 2:
	print 'Require <TAIR10_Transposable_Elements.txt>, output one single bigbed file'
	sys.exit()


cid = 1
fout = open('repeat.bed','w')
with open(sys.argv[1]) as fin:
	fin.readline()
	for line in fin:
		lst = line.rstrip().split('\t')
		fout.write('Chr{0}\t{1}\t{2}\t{3},{4}\t{5}\t{6}\n'.format(
			lst[0].split('T')[1],
			lst[2], lst[3], lst[4], lst[5],
			cid,
			'+' if lst[1]=='true' else '-'))
		cid += 1
fout.close()

os.system('bedSort repeat.bed repeat.bed')
os.system('bedToBigBed repeat.bed /home/xzhou/data/tair10/chromsize repeat.bigBed')
