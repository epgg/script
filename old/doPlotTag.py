import os
import sys


# make vertical image of track attribute types
os.system("/home/xzhou/subtleKnife/script/plotTag \"DNA Methylation\" v")
os.system("/home/xzhou/subtleKnife/script/plotTag \"Histone Modification\" v")
os.system("/home/xzhou/subtleKnife/script/plotTag \"Other Epigenetic Marks\" v")
os.system("/home/xzhou/subtleKnife/script/plotTag Individual v")
os.system("/home/xzhou/subtleKnife/script/plotTag Gender v")
os.system("/home/xzhou/subtleKnife/script/plotTag Disease v")
os.system("/home/xzhou/subtleKnife/script/plotTag Institution v")
os.system("/home/xzhou/subtleKnife/script/plotTag \"Cell Type\" v")
os.system("/home/xzhou/subtleKnife/script/plotTag \"Tissue Organ\" v")


mark = set()
sample = set()
with open("/home/xzhou/kent/src/hg/subtleKnife/config/dataTrackGroupings.tab") as fin:
	for line in fin:
		lst = line.rstrip().split('\t')
		mark.add(lst[1])
		sample.add(lst[2])


for t in mark:
	os.system("/home/xzhou/subtleKnife/script/plotTag \"{0}\" v".format(t))
for t in sample:
	os.system("/home/xzhou/subtleKnife/script/plotTag \"{0}\" h".format(t))

