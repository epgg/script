
infile='/home/xzhou/data/spombe201203/pombe_09052011.gff'

outfile='repeat'

fout=open(outfile,'w')
i=1
with open(infile) as fin:
	for line in fin:
		lst=line.split('\t')
		if lst[2]=='repeat_region' or lst[2]=='LTR':
			tt=lst[8].split(' ; ')
			h={}
			for j in range(len(tt)):
				x=tt[j].split(' ',1)
				if len(x)==2:
					h[x[0]]=x[1]
			desc=''
			if 'note' in h:
				desc=h['note']
			elif 'repeat_region' in h:
				desc=h['repeat_region']
			elif 'LTR' in h:
				desc=h['LTR']
			#desc=tt[0].split(' ')[1]
			fout.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(lst[0], lst[3],lst[4],
				desc.replace('"',''), i, lst[6]))
			i+=1
print i

'''
import os
outfile2='repeat'
os.system('bedSort '+outfile+' '+outfile2)
os.system('bgzip '+outfile2)
os.system('tabix -p bed '+outfile2+'.gz')
'''
