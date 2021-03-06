#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define chrSizeFile2 "/home/xzhou/data/hg19/chr_len2"
#define chrSizeFile "/home/xzhou/data/hg19/chr_len3"
#define nocontent "\\N"
#define nostrand '0'

struct region
    {
    struct region *next;
    int start;
    int stop;
    char strand; // set to '0' when no strand info
    char *name; // set to NULL when no name info
    };
struct node
    {
    struct node *next;
    char *name; // chr1
    char *name2; // chr01
    struct region *regionSl;
    };

struct node *getNode(struct node *sl, char *what)
{
for(; sl!=NULL; sl=sl->next)
    {
    if(strcmp(sl->name, what) == 0)
        return sl;
    }
return NULL;
}
struct node *getNode2(struct node *sl, char *what)
{
for(; sl!=NULL; sl=sl->next)
    {
    if(strcmp(sl->name2, what) == 0)
        return sl;
    }
return NULL;
}




int max(int a, int b)
{
return (a >= b) ? a : b;
}
int min(int a, int b)
{
return (a >= b) ? b : a;
}

void slReverse(struct region **sl)
{
struct region *new=NULL, *prev=*sl, *curr;
while(prev != NULL)
    {
    curr = prev->next;
    prev->next = new;
    new = prev;
    prev = curr;
    }
*sl = new;
}

void slFree(struct region *sl)
{
struct region *prev=sl, *curr;
while(prev != NULL)
    {
    curr = prev->next;
    free(prev);
    prev = curr;
    }
}




int main(int argc, char *argv[])
{
if(argc != 3)
    {
    printf("Usage: %s\n"
           "\t<input \"bed\" file generated by refFlat2bed.c>\n"
	   "\t<output covering file>\n", argv[0]);
    exit(0);
    }

char *inFile = argv[1];
char *outFile = argv[2];


puts("load chr size file, make holder...");
struct node *chrSl = NULL;
FILE *fin = fopen(chrSizeFile2, "r");
if(fin == NULL)
    {
    printf("%m: %s\n", chrSizeFile2);
    exit(0);
    }
size_t s = 1;
char *line = malloc(1), *tok;
char delim[] = "\t\n";
while(getline(&line, &s, fin) != -1)
    {
    tok = strtok(line, delim);
    struct node *this = malloc(sizeof(struct node));
    asprintf(&this->name, "%s", tok);
    strtok(NULL, delim);
    asprintf(&this->name2, "%s", strtok(NULL, delim));
    this->regionSl = NULL;
    this->next = chrSl;
    chrSl = this;
    }
fclose(fin);


char *tmpFile = tempnam(".", NULL);

printf("replacing chr name of %s for natural sorting...\n", inFile);
struct node *chr = chrSl;
fin = fopen(inFile, "r");
FILE *fout = fopen(tmpFile, "w");
int bad = 0;
while(getline(&line, &s, fin) != -1)
    {
    tok = strtok(line, delim);
    if(strcmp(chr->name, tok) != 0)
        {
        if((chr=getNode(chrSl, tok)) == NULL)
	    {
	    chr = chrSl;
	    bad++;
	    continue;
	    }
	}
    fprintf(fout, "%s", chr->name2);
    fprintf(fout, "\t%s", strtok(NULL, delim));
    fprintf(fout, "\t%s", strtok(NULL, delim));
    fprintf(fout, "\t%s", strtok(NULL, delim));
    fprintf(fout, "\t%s\n", strtok(NULL, delim));
    }
fclose(fin);
fclose(fout);
if(bad > 0) printf("%d items with unknown chr name...\n", bad);


char *command;
puts("bedSort on this file to get natural order...");
asprintf(&command, "bedSort %s %s", tmpFile, tmpFile);
system(command);

puts("bedItemOverlapCount on resulting file...");
asprintf(&command, "bedItemOverlapCount -chromSize=%s hg19 %s > %s", chrSizeFile, tmpFile, outFile);
system(command);

/*
puts("bedSort again on this 'bedGraph' file...");
asprintf(&command, "bedSort %s %s", outFile, outFile);
system(command);
*/


puts("merge connected items in 'bedGraph' file...");
if((fin = fopen(outFile, "r")) == NULL)
    {
    printf("%m: %s\n", outFile);
    exit(0);
    }
if((fout = fopen(tmpFile, "w")) == NULL)
    {
    printf("%m: %s\n", tmpFile);
    exit(0);
    }
char *lastChr = NULL;
int lastStart, lastStop;
while(getline(&line, &s, fin) != -1)
    {
    tok = strtok(line, delim);
    int start = strtol(strtok(NULL, delim), NULL, 0);
    int stop = strtol(strtok(NULL, delim), NULL, 0);
    if(lastChr == NULL)
        {
	asprintf(&lastChr, "%s", tok);
	lastStart = start;
	lastStop = stop;
	}
    else
        {
        if(strcmp(lastChr, tok) == 0)
            {
	    if(lastStop == start)
	        lastStop = stop;
            else
	        {
		fprintf(fout, "%s\t%d\t%d\n", lastChr, lastStart, lastStop);
		lastStart = start;
		lastStop = stop;
		}
	    }
	else
	    {
	    fprintf(fout, "%s\t%d\t%d\n", lastChr, lastStart, lastStop);
	    asprintf(&lastChr, "%s", tok);
	    lastStart = start;
	    lastStop = stop;
	    }
        }
    }
fclose(fin);
fclose(fout);




puts("load input file...");
fin = fopen(inFile, "r");
if(fin == NULL)
    {
    printf("%m: %s\n", inFile);
    exit(0);
    }
struct region *r;
while(getline(&line, &s, fin) != -1)
    {
    tok = strtok(line, delim);
    if(strcmp(tok, chr->name) != 0)
        {
        if((chr=getNode(chrSl, tok)) == NULL)
	    {
	    chr = chrSl;
	    continue;
	    }
	}
    r = malloc(sizeof(struct region));
    r->start = strtol(strtok(NULL, delim), NULL, 0);
    r->stop = strtol(strtok(NULL, delim), NULL, 0);
    tok = strtok(NULL, delim);
    if(strcmp(tok, nocontent) == 0)
        r->strand = nostrand;
    else
        r->strand = tok[0];
    tok = strtok(NULL, delim);
    if(strcmp(tok, nocontent) == 0)
        r->name = NULL;
    else
        asprintf(&r->name, "%s", tok);
    r->next = chr->regionSl;
    chr->regionSl = r;
    }
fclose(fin);


puts("read \"bedGraph\" file, make output...");
if((fin = fopen(tmpFile, "r")) == NULL)
    {
    printf("%m: %s\n", tmpFile);
    exit(0);
    }
// see dbSchema.dia for file format
if((fout = fopen(outFile, "w")) == NULL) 
    {
    printf("%m: %s\n", outFile);
    exit(0);
    }

// each line of "bedGraph" file is a covering region
int idx = 0; // id of covering regions
while(getline(&line, &s, fin) != -1)
    {
    tok = strtok(line, delim);
    if(strcmp(chr->name2, tok) != 0)
        {
        if((chr=getNode2(chrSl, tok)) == NULL)
	    {
	    printf("unknown chr name: %s this shouldn't happen\n", tok);
	    chr = chrSl;
	    continue;
	    }
	}
    int start = strtol(strtok(NULL, delim), NULL, 0);
    int stop = strtol(strtok(NULL, delim), NULL, 0);
    struct region *rsl = NULL; // to hold items constituting this covering region
    int itemNumber = 0;
    for(r=chr->regionSl; r!=NULL; r=r->next)
        {
	if(min(stop,r->stop) > max(start,r->start))
	    {
	    struct region *r2 = malloc(sizeof(struct region));
	    r2->start = r->start;
	    r2->stop = r->stop;
	    r2->strand = r->strand;
	    r2->name = r->name;
	    r2->next = rsl;
	    rsl = r2;
	    itemNumber++;
	    }
	else if(start > r->stop)
	    break;
	}
    if(itemNumber == 0)
        {
        printf("no item found for a region: %s:%d-%d\n", chr->name, start,stop);
	exit(0);
	}
    fprintf(fout, "%d\t%s\t%d\t%d\t%d\t", ++idx, chr->name, start, stop, itemNumber);
    slReverse(&rsl);
    struct region *r2 = rsl;
    for(; r2!=NULL; r2=r2->next)
        {
        fprintf(fout, "%d:%d:", r2->start, r2->stop);
	if(r2->strand != nostrand)
	    fputc(r2->strand, fout);
	    //fprintf(fout, "%c", r2->strand);
	fputc(':', fout);
	if(r2->name != NULL)
	    fprintf(fout, "%s", r2->name);
	fputc(',', fout);
	}
    fputs("\n", fout);
    slFree(rsl);
    }
fclose(fin);
fclose(fout);

unlink(tmpFile);

}
