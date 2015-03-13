import glob,os,sys


if len(sys.argv)!=3:
	print '<input dir> <track name>'
	sys.exit()


indir,tkname=sys.argv[1:]


coord=[]

outfile='out/'+tkname
fout=open(outfile,'w')
iid=1
for f in glob.glob(indir+'*'):
	# file name contain coordinate like 'chr10_43262783-43545128_...'
	fbn=os.path.basename(f)
	lst=fbn.split('_')
	if len(lst)<3:
		raise 'wrong file name '+fbn
	lst2=lst[1].split('-')
	if len(lst2)!=2:
		raise 'wrong coord from file name '+fbn
	coord.append((lst[0], lst2[0], lst2[1]))
	
	# 1st line, cols of matrix
	with open(f) as fin:
		line=fin.readline()
		lst=line.strip().split('\t')
		clst=[]
		for x in lst:
			xx=x.split('|')[2].split(':')
			xxx=xx[1].split('-')
			clst.append((xx[0],int(xxx[0]),int(xxx[1])))
		for line in fin:
			lst=line.rstrip().split('\t')
			x=lst[0].split('|')[2].split(':')
			xx=x[1].split('-')
			start=int(xx[0])
			stop=int(xx[1])
			# x[0] : xx[0] - xx[1]
			for i in range(len(clst)):
				if lst[i+1]=='0': continue
				fout.write('{0}\t{1}\t{2}\t{3}:{4}-{5},{6}\t{7}\t{8}\n'.format(
					x[0],start,stop,
					clst[i][0],clst[i][1],clst[i][2],
					lst[i+1],
					iid,
					'.' if x[0]!=clst[i][0] else ('+' if clst[i][1]>start else '-')))
				iid+=1
				fout.write('{0}\t{1}\t{2}\t{3}:{4}-{5},{6}\t{7}\t{8}\n'.format(
					clst[i][0],clst[i][1],clst[i][2],
					x[0],start,stop,
					lst[i+1],
					iid,
					'.' if x[0]!=clst[i][0] else ('+' if clst[i][1]<start else '-')))
				iid+=1
fout.close()

os.system('bedSort {0} {0}'.format(outfile,outfile))
os.system('bgzip {0}'.format(outfile))
os.system('tabix -p bed {0}.gz'.format(outfile))

lst=[]
for c in coord:
	lst.append('{0}:{1}-{2}'.format(c[0],c[1],c[2]))
print '{0}\t{1}'.format(tkname,','.join(lst))
print
