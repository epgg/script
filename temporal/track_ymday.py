fout=open('ymd','w')
for i in range(1962,2014):
	fout.write('''{0}\t1\t31
{0}\t2\t{1}
{0}\t3\t31
{0}\t4\t30
{0}\t5\t31
{0}\t6\t30
{0}\t7\t31
{0}\t8\t31
{0}\t9\t30
{0}\t10\t31
{0}\t11\t30
{0}\t12\t31\n'''.format(str(i), '29' if i%4==0 else '28'))
fout.close()


fout=open('xx','w')
with open('ymd') as fin:
	for line in fin:
		lst=line.rstrip().split('\t')
		month=int(lst[1])
		day=int(lst[2])
		i+=1
		fout.write('{0}\t{1}\t{2}\t.\t{3}\t.\n'.format(lst[0],month*100+1,month*100+day,i))
fout.close()

import os
os.system('sort -k1,1 -k2,2n xx > yy')
os.system('bgzip yy -c > yearmonthday.gz')
os.system('tabix -p bed yearmonthday.gz')
