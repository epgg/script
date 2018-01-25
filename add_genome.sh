#!/bin/bash
# Daofeng
# last modified: May,6,2015

#gemome='danRer10'
#genome='canFam3'
#genome='galGal4'
#genome='rn6'
#genome='ce10'
genome='dm6'
#oldgenome='danRer7'

: <<'END'
END
mkdir ${genome}
cd ${genome}/
wget http://hgdownload.soe.ucsc.edu/goldenPath/${genome}/bigZips/${genome}.2bit
hgGcPercent -win=5 -file=gc5Base.wig -wigOut ${genome} ${genome}.2bit -noDots
twoBitInfo ${genome}.2bit ${genome}.size
wigToBigWig gc5Base.wig ${genome}.size gc5Base.bigWig  # this step need large memory
twoBitToFa ${genome}.2bit ${genome}.fa
python /srv/epgg/data/subtleKnife/script/fa2tabix.py ${genome}.fa ${genome}
rm -f gc5Base.wig 
wget http://hgdownload.soe.ucsc.edu/goldenPath/${genome}/database/refGene.txt.gz
wget http://hgdownload.soe.ucsc.edu/goldenPath/${genome}/database/refLink.txt.gz
wget http://hgdownload.soe.ucsc.edu/goldenPath/${genome}/database/xenoRefGene.txt.gz
wget http://hgdownload.soe.ucsc.edu/goldenPath/${genome}/database/cytoBandIdeo.txt.gz
gunzip *.txt.gz
python /srv/epgg/data/subtleKnife/script/cytoband.py cytoBandIdeo.txt > cytoband 
python /srv/epgg/data/subtleKnife/script/hammock/ucsc_simplegene.py refGene.txt refGene > load.sql
python /srv/epgg/data/subtleKnife/script/hammock/ucsc_simplegene.py xenoRefGene.txt xenoRefGene >> load.sql
mkdir browserLoad
mv load.sql *_load browserLoad/

wget http://hgdownload.soe.ucsc.edu/goldenPath/${genome}/database/cpgIslandExt.txt.gz
python /srv/epgg/data/subtleKnife/script/cpgIsland.py
bgzip cpgisland
tabix -p bed cpgisland.gz
python /srv/epgg/data/subtleKnife/script/scaffoldInfo.py ${genome}.size scaffoldInfo
#total base:  1371719383
#chromosome:,  26
#contig:,  1035
#
mkdir config
mv scaffoldInfo config/
mv cytoband config/

mkdir rmsk
cd rmsk
wget http://hgdownload.soe.ucsc.edu/goldenPath/${genome}/database/rmsk.txt.gz
python /srv/epgg/data/subtleKnife/script/rmsk2ensembleCatHam.py /srv/epgg/data/subtleKnife/script/cat_rmsk rmsk.txt.gz 
bgzip rmsk_all
tabix -p bed rmsk_all.gz


echo "#both on test and public"
echo "mkdir /srv/epgg/data/data/subtleKnife/${genome}"
echo "mkdir /srv/epgg/data/data/subtleKnife/${genome}/config"
echo "mkdir /srv/epgg/data/data/subtleKnife/${genome}/session"
echo "chmod 777 /srv/epgg/data/data/subtleKnife/${genome}/session"
echo "# both end"

echo "#on test"
echo "# at /srv/epgg/data/dli/add_${genome}/config"
echo "mkdir ~/eg/config/${genome}"
echo "mv * ~/eg/config/${genome}/"
echo "# on public"
echo "#cp /srv/epgg/data/subtleKnife/config/${oldgenome}/makeDb.sql ."
echo "#cp /srv/epgg/data/subtleKnife/config/${oldgenome}/tracks.json ."
echo "mysql -u hguser -phguser -e 'create database ${genome};'"
echo "# at /srv/epgg/data/dli/add_${genome}/config"
echo "cat makeDb.sql | mysql -u hguser -phguser ${genome} --local-infile=1"
echo "cat /srv/epgg/data/subtleKnife/config/sessionUtils.sql | mysql -u hguser -phguser ${genome} --local-infile=1"
echo "# at /srv/epgg/data/data/browserLoad/${genome}"
echo "cat load.sql | mysql -u hguser -phguser ${genome} --local-infile=1"
echo "ln -s /srv/epgg/data/data/subtleKnife/${genome}/ /var/www/d/"
echo "scp ${genome}.gz* 10.200.0.12:/srv/epgg/data/data/subtleKnife/seq/"
echo "scp ${genome}.gz* 10.200.0.11:/srv/epgg/data/data/subtleKnife/seq/"
echo "scp *.gz* 10.200.0.11:/srv/epgg/data/data/subtleKnife/${genome}/"
echo "scp *.gz* 10.200.0.12:/srv/epgg/data/data/subtleKnife/${genome}/" # gene tbi files also need be locally
echo "scp *.bigWig 10.200.0.11:/srv/epgg/data/data/subtleKnife/${genome}/"
echo "scp rmsk/rmsk_all.gz* 10.200.0.11:/srv/epgg/data/data/subtleKnife/${genome}/"
echo "## for .8"
echo "#mysql> GRANT ALL privileges ON galGal4.* TO 'hguser'@'%' IDENTIFIED BY 'hguser' WITH GRANT OPTION;"
echo "#mysql> FLUSH PRIVILEGES;"
echo "#makeDb.sql need change default location after 1st load, then reload"
echo "#put tracks.json on genome/config"
echo "## at pub"
echo "#mkdir /srv/epgg/data/data/browserLoad/${genome}"
#echo "#mkdir /srv/epgg/data/data/browserLoad/canFam3"
#echo "#mkdir /srv/epgg/data/data/browserLoad/galGal4"

