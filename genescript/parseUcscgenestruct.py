
def parse(lst,firstisbin):
	a=0 if firstisbin else -1
	id_chrom=2+a
	id_strand=3+a
	id_start=4+a
	id_stop=5+a
	id_cdsstart=6+a
	id_cdsstop=7+a
	id_exoncount=8+a
	id_exonstarts=9+a
	id_exonstops=10+a
	id_name2=12+a
	ss=lst[id_strand]
	gene={'chrom':lst[id_chrom],
		'start':lst[id_start],
		'stop':lst[id_stop],
		'strand':ss}

	if len(lst)>12 and len(lst[id_name2])>0:
		gene['name2']=lst[id_name2]

	lst1=[int(x) for x in lst[id_exonstarts][:-1].split(',')]
	lst2=[int(x) for x in lst[id_exonstops][:-1].split(',')]

	cdsstart=int(lst[id_cdsstart])
	cdsstop=int(lst[id_cdsstop])

	if cdsstart==cdsstop:
		lst=[]
		for i in range(len(lst1)):
			lst.append([lst1[i],lst2[i]])
		gene['thin']=lst
		return gene
	
	thin=[]
	thick=[]
	for i in range(len(lst1)):
		start=lst1[i]
		stop=lst2[i]
		if stop<=cdsstart:
			thin.append([start,stop])
		elif stop<=cdsstop:
			if start<cdsstart:
				thin.append([start,cdsstart])
				thick.append([cdsstart,stop])
			else:
				thick.append([start,stop])
		else:
			if start<cdsstart:
				# engulf
				thin.append([start,cdsstart])
				thin.append([cdsstop,stop])
				thick.append([cdsstart,cdsstop])
			else:
				if start<cdsstop:
					thick.append([start,cdsstop])
					thin.append([cdsstop,stop])
				else:
					thin.append([start,stop])
	if len(thin)>0:
		gene['thin']=thin
	if len(thick)>0:
		gene['thick']=thick
	return gene
