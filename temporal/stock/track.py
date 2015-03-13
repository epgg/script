import os

with open('/home/xzhou/subtleKnife/config/temporal_day/stock') as fin:
	for line in fin:
		stock=line.rstrip()
		with open('/home/xzhou/data/stock/table.csv?s='+stock) as fin2:
			fout=open('xx','w')
			fin2.readline()
			for line2 in fin2:
				lst=line2.rstrip().split(',')
				tt=lst[0].split('-')
				month=int(tt[1])
				day=int(tt[2])
				fout.write('{0}\t{1}\t{2}\t{3}\n'.format(tt[0],str(month*100+day),str(month*100+day+1),lst[4]))
			fout.close()
			os.system('sort -k1,1 -k2,2n xx > yy')
			os.system('bgzip yy -c > '+stock+'.gz')
			os.system('tabix -p bed '+stock+'.gz')
