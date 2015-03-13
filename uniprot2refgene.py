# make association for uniprot name and refgene name

import sys
if len(sys.argv) != 4:
	print '''Usage: {0}
	<refGene.txt file>
	<uniprot trembl .dat file>
	<species name (OS field in uniprot.dat file)>\n'''.format(sys.argv[0])
	sys.exit()


refgenefile, unidatfile, species = sys.argv[1:]

# read target gene names from refGene file
targetgene = set()
with open(refgenefile) as fin:
	for line in fin:
		lst = line.split('\t')
		targetgene.add(lst[1])
		targetgene.add(lst[12])

# go over uniprot file
with open(unidatfile) as fin:
	ac = None
	gn = None
	for line in fin:
		if line.startswith("AC"):
			ac = line.split()[1][:-1]
			#gn = None
		elif line.startswith("GN"):
			if 'Name=' in line:
				gn = line.split('Name=')[1].split(';')[0]
				if gn not in targetgene:
					gn = None
		elif line.startswith("OS"):
			if species in line:
				if gn is not None:
					print '{0}\t{1}'.format(ac, gn)
