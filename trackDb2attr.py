import sys

if len(sys.argv) != 3:
	print 'require input trackDb.ra file, and output file'
	sys.exit()


# first read in trackDb.ra file, store everything in data
data = {}
# key: track name
# val: {}
#    sl: an array of words from short label
#    ...and other tags from metadata (optional)
tkname = ''

cellname = {
'AL':['adult liver', 'liver'],
'AK':['adult kidney', 'kidney'],
'AN':['adipose nuclei', 'fat'],
'CM':['colonic mucosa','colon'],
'BreLum':['breast luminal epithelial cells','breast'],
'BreMyo':['breast myoepithelial cells','breast'],
'BreSte':['breast stem cells','breast'],
'BrevHM':['breast vHMEC','breast'],
'BrevHMC':['breast vHMEC','breast'],
'BMDMSC':['bone marrow derived mesenchymal stem cell','bone marrow'],
'ADMSC':['adipose derived mesenchymal stem cell','fat'],
'CD15':['CD15 primary cells','blood'],
'CD19':['CD19 primary cells','blood'],
'CD3':['CD3 primary cells','blood'],
'CD34':['CD34 primary cells','blood'],
'MCD34':['mobilized CD34 primary cells','blood'],
'CD4M':['CD4 memory primary cells','blood'],
'MCD4':['mobilized CD4 primary cells','blood'],
'CD4N':['CD4 naive primary cells','blood'],
'CD8N':['CD8 naive primary cells','blood'],
'DM':['duodenum mucosa','gut'],
'FAG':['fetal adrenal gland','adrenal gland'],
'FB':['fetal brain','brain'],
'FH':['fetal heart','heart'],
'FK':['fetal kidney','kidney'],
'FL':['fetal lung','lung'],
'H1':['H1','\\N'],
'H1BMP4':['H1','\\N'],
'H1 (WA01)':['H1','\\N'],
'H9':['H9','\\N'],
'HUES1':['HUES','\\N'],
'HUES28':['HUES','\\N'],
'HUES3':['HUES','\\N'],
'HUES48':['HUES','\\N'],
'HUES49':['HUES','\\N'],
'HUES53':['HUES','\\N'],
'HUES6':['HUES','\\N'],
'HUES62':['HUES','\\N'],
'HUES63':['HUES','\\N'],
'HUES64':['HUES','\\N'],
'HUES65':['HUES','\\N'],
'HUES66':['HUES','\\N'],
'HUES8':['HUES','\\N'],
'HUES9':['HUES','\\N'],
'ESI3':['hES-I3','\\N'],
'hES-I3':['hES-I3','\\N'],
'hES I3 TESR':['hES-I3','\\N'],
'hiPS-11a':['hiPS-11a','\\N'],
'iPS11a':['hiPS-11a','\\N'],
'iPS11b':['hiPS-11b','\\N'],
'hiPS-15b':['hiPS-15b','\\N'],
'iPS15b':['hiPS-15b','\\N'],
'iPS17a':['hiPS-17a','\\N'],
'iPS17b':['hiPS-17b','\\N'],
'iPS18a':['hiPS-18a','\\N'],
'iPS18b':['hiPS-18b','\\N'],
'iPS18c':['hiPS-18c','\\N'],
'hiPS-18b':['hiPS-18b','\\N'],
'hiPS-18c':['hiPS-18c','\\N'],
'hiPS-20b':['hiPS-20b','\\N'],
'iPS20b':['hiPS-20b','\\N'],
'IMR90':['IMR90','\\N'],
'MSCC':['Muscle Satellite Cultured Cells','muscle'],
'PBM':['peripheral blood mononuclear primary cells','blood'],
'PBMC':['peripheral blood mononuclear primary cells','blood'],
'PI':['pancreatic islets','pancreatic islets'],
'RM':['rectal mucosa','rectum'],
'RSM':['rectal smooth muscle','rectum'],
'SM':['skeletal muscle','skeletal muscle'],
'SMSM':['skeletal muscle','skeletal muscle'],
'SSM':['stomach smooth muscle','stomach'],
'Th17':['Th17','\\N'],
'Treg':['Treg primary cells','\\N'],
'WA-7':['WA-7','\\N'],
'ESWA7':['WA-7','\\N']
}




with open(sys.argv[1]) as fin:
	for line in fin:
		if line.startswith('track '):
			continue
		line = line.strip()
		if line.startswith('track '):
			tkname = line.split()[1][:-1]
			if tkname not in data:
				data[tkname] = {}
			else:
				print tkname+' met before'
		elif line == '':
			tkname = ''
		elif line.startswith('shortLabel '):
			if tkname == '':
				continue
			data[tkname]['sl']= line.rstrip().split()[1:]
		elif line.startswith('metadata'):
			if tkname == '':
				continue
			lst = line.split('=')
			for i,tt in enumerate(lst[:-1]):
				lst2 = tt.split()
				lst3 = lst[i+1].split()
				data[tkname][lst2[-1]] = ' '.join(lst3[:-1]).replace('"','')

methylationNames = ('RRBS','MeDIP','MRE','BisulfiteSeq')

fout = open(sys.argv[2],'w')
# fields:
# dna methylation
# histone modification
# other marks
# individual
# gender
# disease
# cell type
# tissue/organ
# institution
for tk in data:
	#fout.write(tk+"\t")
	sl = data[tk]['sl']
	fout.write("{0}\t{1}\t".format(tk,' '.join(sl)))
	if len(sl) < 4:
		print 'wrong:',tk,sl
		sl.append('\\N')
	if 'experiment_type' not in data[tk]:
		# don't have metadata, sl[2] should be mark type
		if sl[2] in methylationNames:
		    fout.write("{0[2]}\t\\N\t\\N\t{0[3]}\t\\N\t\\N\t".format(sl))
		elif sl[2][0] == 'H': # histone?
		    fout.write("\\N\t{0[2]}\t\\N\t{0[3]}\t\\N\t\\N\t".format(sl))
		else: # other marks
			if sl[2] == 'Input':
				fout.write("\\N\t\\N\tChIP-Seq Input\t{0[3]}\t\\N\t\\N\t".format(sl))
		    	else:
				fout.write("\\N\t\\N\t{0[2]}\t{0[3]}\t\\N\t\\N\t".format(sl))
		if sl[1] in cellname: # cell and tissue
			fout.write("{0[0]}\t{0[1]}\t".format(cellname[sl[1]]))
		else:
			fout.write("\\N\t\\N\t")
		fout.write(sl[0]+'\n') # institution
		continue
	tmp = data[tk]['experiment_type']
	# mark type
	if tmp == 'DNA Methylation':
		if 'MeDIP' in sl:
			fout.write("MeDIP\t\\N\t\\N\t")
		elif 'MRE' in sl:
			fout.write("MRE\t\\N\t\\N\t")
		elif 'BisulfiteSeq' in sl:
			fout.write("BisulfiteSeq\t\\N\t\\N\t")
		else:
			print 'unknown dna methylation type:',tk,sl
			sys.exit()
	elif tmp.startswith("Histone"):
		lst = tmp.split()
		if(len(lst) != 2):
			print 'unknown histone:',tmp
			sys.exit()
		else:
			fout.write("\\N\t{0}\t\\N\t".format(lst[1]))
	else:
		fout.write("\\N\t\\N\t{0}\t".format(tmp))
	# individual
	if 'donor_id' in data[tk]:
		fout.write(data[tk]['donor_id']+'\t')
	else:
		fout.write('\\N\t')
	# gender
	if 'sex' in data[tk]:
		fout.write(data[tk]['sex']+'\t')
	elif 'Sex' in data[tk]:
		fout.write(data[tk]['Sex']+'\t')
	elif 'donor_sex' in data[tk]:
		fout.write(data[tk]['donor_sex']+'\t')
	else:
		fout.write('\\N\t')
	# disease
	if 'disease' in data[tk]:
		fout.write(data[tk]['disease']+'\t')
	else:
		fout.write('\\N\t')
	# cell and tissue type
	if sl[1] in cellname:
		fout.write('{0[0]}\t{0[1]}\t'.format(cellname[sl[1]]))
	else:
		if 'cell_type' in data[tk]:
			print '{0}: {1} -> {2}'.format(tk, sl[1], data[tk]['cell_type'])
			print 'register it in the script'
			continue
		if 'line' in data[tk]:
			print '{0}: {1} -> {2}'.format(tk, sl[1], data[tk]['line'])
			print 'register it in the script'
			continue
		print '{0}: {1} unknown cell type'.format(tk, sl[1])
	# institution
	fout.write(sl[0])
	fout.write("\n")
fout.close()
