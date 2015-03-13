#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define chrSizeFile "/home/xzhou/data/hg19/chr_len2"

struct node
    {
    struct node *next;
    char *name;
    int length;
    };

int getChrLength(struct node *sl, char *what)
{
for(; sl!=NULL; sl=sl->next)
    {
    if(strcmp(sl->name, what) == 0)
        return sl->length;
    }
return 0;
}



int main(int argc, char *argv[])
{

if(argc != 2)
    {
    printf("Require refGene.txt file, output file will be:\n"
        "\tpromoter.bed, utr5.bed, exons.bed, introns.bed, genebody.bed, utr3.bed\n");
    exit(0);
    }


// load chr size file
struct node *chrSl = NULL;
FILE *fin = fopen(chrSizeFile, "r");
if(fin == NULL)
    {
    printf("%m: %s\n", chrSizeFile);
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
    this->length = strtol(strtok(NULL, delim), NULL, 0);
    this->next = chrSl;
    chrSl = this;
    }
fclose(fin);


char *inFile = argv[1];
fin = fopen(inFile, "r");
if(fin == NULL)
    {
    printf("%m: %s\n", inFile);
    exit(0);
    }
FILE *promoterF = fopen("promoter.bed", "w");
FILE *utr5F = fopen("utr5.bed", "w");
FILE *exonF = fopen("exons.bed", "w");
FILE *intronF = fopen("introns.bed", "w");
FILE *gbF = fopen("genebody.bed", "w");
FILE *utr3F = fopen("utr3.bed", "w");
int pI=0, u5I=0, u3I=0, eI=0, iI=0, gI=0;

/*
  `bin` smallint(5) unsigned NOT NULL default '0',
  `name` varchar(255) NOT NULL default '',
  `chrom` varchar(255) NOT NULL default '',
  `strand` char(1) NOT NULL default '',
  `txStart` int(10) unsigned NOT NULL default '0',
  `txEnd` int(10) unsigned NOT NULL default '0',
  `cdsStart` int(10) unsigned NOT NULL default '0',
  `cdsEnd` int(10) unsigned NOT NULL default '0',
  `exonCount` int(10) unsigned NOT NULL default '0',
  `exonStarts` longblob NOT NULL,
  `exonEnds` longblob NOT NULL,
  `id` int(10) unsigned NOT NULL default '0',
  `name2` varchar(255) NOT NULL default '',
  `cdsStartStat` enum('none','unk','incmpl','cmpl') NOT NULL default 'none',
  `cdsEndStat` enum('none','unk','incmpl','cmpl') NOT NULL default 'none',
  `exonFrames` longblob NOT NULL,
 */
char *name, *chr, *exonstarts, *exonstops;
char delim2[] = ",";
while(getline(&line, &s, fin) != -1)
    {
    strtok(line, delim);
    strtok(NULL, delim);
    // chromosome
    if((tok=strtok(NULL, delim)) == NULL)
        {
	puts("expecting chrom got null");
	exit(0);
	}
    int chrLen = getChrLength(chrSl, tok);
    if(chrLen == 0)
        continue;
    asprintf(&chr, "%s", tok);
    // strand
    if((tok=strtok(NULL, delim)) == NULL)
        {
	puts("expecting strand got null");
	exit(0);
	}
    char strand = tok[0];
    // tx start
    if((tok=strtok(NULL, delim)) == NULL)
        {
	puts("expecting tx start got null");
	exit(0);
	}
    int txStart = strtol(tok, NULL, 0);
    // tx stop
    if((tok=strtok(NULL, delim)) == NULL)
        {
	puts("expecting tx stop got null");
	exit(0);
	}
    int txStop = strtol(tok, NULL, 0);


    // cds start
    if((tok=strtok(NULL, delim)) == NULL)
        {
	puts("expecting cds start got null");
	exit(0);
	}
    int cdsStart = strtol(tok, NULL, 0);
    // cds stop
    if((tok=strtok(NULL, delim)) == NULL)
        {
	puts("expecting cds stop got null");
	exit(0);
	}
    int cdsStop = strtol(tok, NULL, 0);
    // exon count
    if((tok=strtok(NULL, delim)) == NULL)
        {
	puts("expecting exon count got null");
	exit(0);
	}
    int exonCount = strtol(tok, NULL, 0);
    // exon starts
    if((tok=strtok(NULL, delim)) == NULL)
        {
	puts("expecting exon starts got null");
	exit(0);
	}
    asprintf(&exonstarts, "%s", tok);
    // exon stops
    if((tok=strtok(NULL, delim)) == NULL)
        {
	puts("expecting exon stops got null");
	exit(0);
	}
    asprintf(&exonstops, "%s", tok);
    strtok(NULL, delim);
    // gene name
    if((tok=strtok(NULL, delim)) == NULL)
        {
	puts("expecting name got null");
	exit(0);
	}
    asprintf(&name, "%s", tok);


    /**** OUTPUT *****/
    // gene body
    fprintf(gbF, "%s\t%d\t%d\t%c\t%s\t%d\n", chr, txStart, txStop, strand, name, gI++);

    // promoter
    if(strand == '+')
        fprintf(promoterF, "%s\t%d\t%d\t+\t%s\t%d\n", chr, (txStart > 3000) ? txStart-3000 : 0, txStart, name, pI++);
    else
        fprintf(promoterF, "%s\t%d\t%d\t-\t%s\t%d\n", chr, txStop, (txStop+3000>chrLen)? chrLen-1 : txStop+3000, name, pI++);

    // don't process non-coding genes for exons/introns/UTRs
    if(cdsStart == cdsStop)
        {
	continue;
	}

    // 5' 3' utr
    if(strand == '+')
        {
	if(txStart < cdsStart)
	    fprintf(utr5F, "%s\t%d\t%d\t+\t%s\t%d\n", chr, txStart, cdsStart, name, u5I++);
	if(txStop > cdsStop)
	    fprintf(utr3F, "%s\t%d\t%d\t+\t%s\t%d\n", chr, cdsStop, txStop, name, u3I++);
	}
    else
        {
	if(txStart < cdsStart)
	    fprintf(utr3F, "%s\t%d\t%d\t+\t%s\t%d\n", chr, txStart, cdsStart, name, u3I++);
	if(txStop > cdsStop)
	    fprintf(utr5F, "%s\t%d\t%d\t+\t%s\t%d\n", chr, cdsStop, txStop, name, u5I++);
	}
    // exons, introns
    int exonStartCoord[exonCount], exonStopCoord[exonCount];
    int i;
    exonStartCoord[0] = strtol(strtok(exonstarts, delim2), NULL, 0);
    for(i=1; i<exonCount; i++)
	exonStartCoord[i] = strtol(strtok(NULL, delim2), NULL, 0);
    exonStopCoord[0] = strtol(strtok(exonstops, delim2), NULL, 0);
    for(i=1; i<exonCount; i++)
	exonStopCoord[i] = strtol(strtok(NULL, delim2), NULL, 0);
    fprintf(exonF, "%s\t%d\t%d\t%c\t%s\t%d\n", chr, exonStartCoord[0], exonStopCoord[0],strand, name, eI++);
    int intronStart = exonStopCoord[0];
    for(i=1; i<exonCount; i++)
        {
        fprintf(exonF, "%s\t%d\t%d\t%c\t%s\t%d\n", chr, exonStartCoord[i], exonStopCoord[i],strand, name, eI++);
	fprintf(intronF, "%s\t%d\t%d\t%c\t%s\t%d\n", chr, intronStart, exonStartCoord[i], strand, name, iI++);
	intronStart = exonStopCoord[i];
	}
    }
fclose(promoterF);
fclose(utr5F);
fclose(utr3F);
fclose(exonF);
fclose(intronF);
fclose(gbF);


char *command = "bedSort promoter.bed promoter.bed";
system(command);
command = "bedSort utr5.bed utr5.bed";
system(command);
command = "bedSort utr3.bed utr3.bed";
system(command);
command = "bedSort exons.bed exons.bed";
system(command);
command = "bedSort introns.bed introns.bed";
system(command);
command = "bedSort genebody.bed genebody.bed";
system(command);
}
