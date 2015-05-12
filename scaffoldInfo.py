#!/usr/bin/python
# programmer : Daofeng
# usage:

import sys

def main():
    lis1 = []
    lis2 = []
    tb = 0
    try:
        with open(sys.argv[1],"rU") as infile:
            for line in infile:
                t = line.strip().split('\t')
                if '_' in t[0]:
                    lis2.append((t[0], t[1]))
                else:
                    lis1.append((t[0], t[1]))
                tb += int(t[1])
        with open(sys.argv[2],'w') as outfile:
            outfile.write('{}\t{}\t{}\n'.format('ROOT','chromosome', 0))
            outfile.write('{}\t{}\t{}\n'.format('ROOT','other', 0))
            for i in lis1:
                outfile.write('{}\t{}\t{}\n'.format('chromosome',i[0], i[1]))
            for i in lis2:
                outfile.write('{}\t{}\t{}\n'.format('other',i[0], i[1]))

        print 'total base: ', tb
        print 'chromosome:, ', len(lis1)
        print 'contig:, ', len(lis2)
    except IOError,message:
        print >> sys.stderr, "cannot open file",message
        sys.exit(1)

if __name__=="__main__":
    main()


