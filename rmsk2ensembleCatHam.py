import sys,gzip

if len(sys.argv)!=3:
    print '<cateinfo file> <rmsk.txt> output to stdout'
    sys.exit()


cateinfile, rmskfile=sys.argv[1:]

cateinfo={}

with open(cateinfile) as fin:
    for line in fin:
        lst=line.rstrip().split()
        cateinfo[lst[0]]=int(lst[1])

cat = {
1:["SINE - short interspersed nuclear elements","#cc0000"],
2:["LINE - long interspersed nuclear element","#FF6600"],
3:["LTR - long terminal repeat element","#006600"],
4:["DNA transposon","#4A72E8"],
5:["Simple repeat, micro-satellite","#AB833B"],
6:["Satellite repeat","#660000"],
7:["Low complexity repeat","#663333"],
8:["RNA repeat","#cc33ff"],
9:["Other repeats","#488E8E"],
10:["Unknown","#5C5C5C"],
11:["Retroposon","#EA53C4"],
12:["ARTEFACT","#00FFAA"],
}

#bin    swScore milliDiv    milliDel    milliIns    genoName    genoStart   genoEnd genoLeft    strand  repName repClass    repFamily   repStart    repEnd  repLeft id
#585     1504    13      4       13      chr1    10000   10468   -249240153      +       (CCCTAA)n       Simple_repeat   Simple_repeat   1       463     0       1
#585     3612    114     270     13      chr1    10468   11447   -249239174      -       TAR1    Satellite       telo    -399    1712    483     2
#585     437     235     186     35      chr1    11503   11675   -249238946      -       L1MC    LINE    L1      -2236   5646    5449    3
#585     239     294     19      10      chr1    11677   11780   -249238841      -       MER5B   DNA     hAT-Charlie     -74     104     1       4

d = {}
i = 0
#with open(rmskfile) as fin:
with gzip.open(rmskfile, 'rb') as fin, open('rmsk_all', 'w') as fout:
#with gzip.open(rmskfile, 'rb') as fin, open('rmsk_cat', 'w') as fout:
    for line in fin:
        i += 1
        lst=line.rstrip().split('\t')
        if lst[11] in cateinfo:
            l = int(lst[7]) - int(lst[6])
            print >> fout, '{0}\t{1}\t{2}\tname:"{5}",strand:"{6}",scorelst:[{7},{8:.2f},{14:.3f}],details:{{Divergence:"{9:.1%}",Deletion:"{10:.1%}",Insertion:"{11:.1%}","Repbase class":"{12}","Repbase family":"{13}"}},id:{4},category:{3}'.format(lst[5],lst[6],lst[7],cateinfo[lst[11]], i, lst[10], lst[9], lst[1], float(lst[1])/l, float(lst[2])/1000, float(lst[3])/1000, float(lst[4])/1000, lst[11], lst[12], 1-float(lst[2])/1000)
            repcat = cateinfo[lst[11]]
            if repcat not in d:
                d[repcat] = 1
        else:
            print >> sys.stderr,'wrong class?', line
            sys.exit(1)
    
    for i in sorted(d.keys()):
        print >> sys.stdout, '{}:{},'.format(i,cat[i])


