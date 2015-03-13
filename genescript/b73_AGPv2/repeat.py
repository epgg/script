import sys
import os

if len(sys.argv) != 2:
	print 'Require file ZmB73_5a_MTEC_repeats.gff'
	sys.exit()


# 9th field: class=I;subclass=1;order=LTR;superfamily=[RLG] Gypsy;family=flip;type=Type I Transposons/LTR;name=RLG_flip_AC214266_12595


chrname = {'chloroplast':'Pt', 'mitochondrion':'Mt'}

chrsizefile = '/home/xzhou/data/b73_AGPv2/chromsize'


# read file for 1st time to parse order-superfam info
order = {} # name : [fout, id]
sfam = {} # name : [fout, id, order]
with open(sys.argv[1]) as fin:
	fin.readline()
	fin.readline()
	fin.readline()
	fin.readline()
	for line in fin:
		lst = line.rstrip().split('\t')
		oname = None
		fname = None
		for t in lst[8].split(';'):
			t1,t2 = t.split('=')
			if t1 == 'order':
				oname = t2
			elif t1=='superfamily':
				fname = t2
				#fname = t2.split()[1]
		if oname is None or fname is None:
			continue
		if oname not in order:
			order[oname] = [open(oname, 'w'), 1]
		if fname not in sfam:
			sfam[fname] = [open(oname+' '+fname, 'w'), 1, oname]


print 'Order - superfamily structure:'
for f in sfam:
	print '{0}\t{1}'.format(sfam[f][2], f)




# read file for 2nd time to output data
fout = open('MTECrepeats.txt', 'w')
totalid = 1
with open(sys.argv[1]) as fin:
	fin.readline()
	fin.readline()
	fin.readline()
	fin.readline()
	for line in fin:
		lst = line.rstrip().split('\t')
		# need to convert chr name
		chrom = 'chr'+(chrname[lst[0]] if lst[0] in chrname else lst[0])
		oname = None
		fname = None
		name = None
		for t in lst[8].split(';'):
			t1,t2 = t.split('=')
			if t1 == 'order':
				oname = t2
			elif t1=='superfamily':
				fname = t2
				#fname = t2.split()[1]
			elif t1=='name':
				name = t2
		if oname is None or fname is None:
			continue
		# to all repeats
		fout.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(chrom, lst[3], lst[4], '.' if name is None else name, totalid, lst[6]))
		totalid += 1
		# to this superfamily
		sfam[fname][0].write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(chrom, lst[3], lst[4], '.' if name is None else name, sfam[fname][1], lst[6]))
		sfam[fname][1] += 1
		# to this order
		order[oname][0].write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(chrom, lst[3], lst[4], '.' if name is None else name, order[oname][1], lst[6]))
		order[oname][1] += 1


fout.close()
for o in order:
	order[o][0].close()
for f in sfam:
	sfam[f][0].close()


# bed sort and bigbed making
os.system('bedSort MTECrepeats.txt MTECrepeats.txt')
os.system('bedToBigBed MTECrepeats.txt '+chrsizefile+' MTECrepeats.bigBed')
for o in order:
	os.system('bedSort "'+o+'" "'+o+'"')
	os.system('bedToBigBed "'+o+'" '+chrsizefile+' "'+o+'.bigBed"')
for f in sfam:
	fn = sfam[f][2]+' '+f
	os.system('bedSort "'+fn+'" "'+fn+'"')
	os.system('bedToBigBed "'+fn+'" '+chrsizefile+' "'+fn+'.bigBed"')

