#!/usr/bin/python
# programmer : Daofeng
# usage:


import gzip

def main():
    i = 1
    try:
        with gzip.open('cpgIslandExt.txt.gz',"rb") as infile:
            with open('cpgisland','w') as outfile:
                for line in infile:
                    t = line.strip().split('\t')
                    #outfile.write('{}\t{}\t{}\t.\t{}\n'.format(t[1], t[2], t[3], t[4].replace(': ','-')))
                    outfile.write('{}\t{}\t{}\t.\t{}\n'.format(t[1], t[2], t[3], i))
                    i += 1
    except IOError,message:
        print >> sys.stderr, "cannot open file",message
        sys.exit(1)
    

if __name__=="__main__":
    main()


