#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "gd.h"
#include "gdfontmb.h"

int main(int argc, char *argv[])
{

if(argc != 3)
    {
    printf("Usage: %s <word to plot> <orientation *h*orizontal, or *u*pward>\n"
           "word might need to be quoted, image name will be the words itself\n", argv[0]);
    exit(0);
    }


char *word = argv[1];
char orientation = argv[2][0];

int wordPlotLen = strlen(word) * 8;

gdImagePtr im;
if(orientation == 'h')
    im = gdImageCreate(wordPlotLen, 18);
else
    im = gdImageCreate(18, wordPlotLen);

int bg = gdImageColorAllocate(im, 0,153,102);
int charcolor = gdImageColorAllocate(im, 255,255,255);

if(orientation == 'h')
    gdImageString(im, gdFontGetMediumBold(), 2,2, word, charcolor);
else
    gdImageStringUp(im, gdFontGetMediumBold(), 2,wordPlotLen-4, word, charcolor);

char *outfile;
asprintf(&outfile, "%s.png", word);
FILE *fout = fopen(outfile, "wb");
gdImagePng(im, fout);
fclose(fout);

gdImageDestroy(im);

}
