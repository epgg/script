import os

months={}
with open('../monthName') as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		lst2=lst[1].split()
		for s in lst2:
			months[s]=lst[0]


dates={}
with open('../yearlyMonthlyLength') as fin:
	for line in fin:
		if line[0]=='\n': continue
		lst=line.rstrip().split('\t')
		if lst[0] in dates:
			dates[lst[0]][lst[1]]=int(lst[2])+1
		else:
			dates[lst[0]]={lst[1]:int(lst[2])+1}

fout1=open('track2Ft_uscensus','w')
fout2=open('track2Label_uscensus','w')

with open('raw.uscensus') as fin:
	# first line dates
	lst=fin.readline().strip().split('\t')
	datelst=[]
	for s in lst:
		lst2=s.split()
		datelst.append([months[lst2[0]],lst2[1]])

	for line in fin:
		# each line is a track
		# 0: name, 1: label, 2-... data
		lst=line.rstrip().split('\t')
		fname='uscensus_'+lst[0]
		fout1.write(fname+'\t2\n')
		fout2.write(fname+'\t'+lst[1]+'\n')
		fout3=open(fname,'w')
		idx=0
		for s in datelst:
			y=s[1]
			m=s[0]
			v=lst[idx+2]
			idx+=1
			fout3.write('{0}\t{1}01\t{1}{2}\t{3}\n'.format(y,m,dates[y][m],0 if v=='(NA)' else v.replace(',','')))
		fout3.close()
		os.system('sort -k1,1 -k2,2n '+fname+' > xx')
		os.system('/srv/epgg/data/tabix-0.2.6/bgzip xx -c > '+fname+'.gz')
		os.system('/srv/epgg/data/tabix-0.2.6/tabix -p bed '+fname+'.gz')
fout1.close()
fout2.close()
