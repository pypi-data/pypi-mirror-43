# In Uniprot there are 3 types of data:

# gaf2 annotation files (both for SwissProt and the whole dataset) - treat annotations as sets of terms
# gpi annotation files (both for SwissProt and the whole dataset) - treat annotations as an ontology
# gene information (mapping, ...)

# these are the files to be downloaded
# ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/HUMAN/gene_association.goa_human.gz
# ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/MOUSE/gene_association.goa_mouse.gz
# ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/FLY/gene_association.goa_fly.gz
# ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/ARABIDOPSIS/gene_association.goa_arabidopsis.gz
# ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/RAT/gene_association.goa_rat.gz
# ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/WORM/gene_association.goa_worm.gz
# ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/ZEBRAFISH/gene_association.goa_zebrafish.gz

# Download entire folder
#wget -r ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/HUMAN/
#mv ftp.ebi.ac.uk/pub/databases/GO/goa/HUMAN/* .
#rm -frv mv ftp.ebi.ac.uk

# Here we only extract gaf2 files
# mkdir Uniprot
# cd Uniprot



###########
# OLD versions
############


# wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/HUMAN/gene_association.goa_human.gz # old version
# OUTFILE=GO_gene_association.goa_human_`date "+%Y.%m.%d"`.gz # old version
# mv gene_association.goa_human.gz $OUTFILE # old version
# gunzip -k $OUTFILE

# wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/MOUSE/gene_association.goa_mouse.gz
# OUTFILE=GO_gene_association.goa_mouse_`date "+%Y.%m.%d"`.gz
# mv gene_association.goa_mouse.gz $OUTFILE
# # gunzip -k $OUTFILE

# wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/FLY/gene_association.goa_fly.gz
# OUTFILE=GO_gene_association.goa_fly_`date "+%Y.%m.%d"`.gz
# mv gene_association.goa_fly.gz $OUTFILE
# # gunzip -k $OUTFILE

# wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/ARABIDOPSIS/gene_association.goa_arabidopsis.gz
# OUTFILE=GO_gene_association.goa_arabidopsis_`date "+%Y.%m.%d"`.gz
# mv gene_association.goa_arabidopsis.gz $OUTFILE
# # gunzip -k $OUTFILE

# wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/RAT/gene_association.goa_rat.gz
# OUTFILE=GO_gene_association.goa_rat_`date "+%Y.%m.%d"`.gz
# mv gene_association.goa_rat.gz $OUTFILE
# # gunzip -k $OUTFILE

# wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/WORM/gene_association.goa_worm.gz
# OUTFILE=GO_gene_association.goa_worm_`date "+%Y.%m.%d"`.gz
# mv gene_association.goa_worm.gz $OUTFILE
# # gunzip -k $OUTFILE

# wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/ZEBRAFISH/gene_association.goa_zebrafish.gz
# OUTFILE=GO_gene_association.goa_zebrafish_`date "+%Y.%m.%d"`.gz
# mv gene_association.goa_zebrafish.gz $OUTFILE
# # gunzip -k $OUTFILE



#################
# NEW VERSIONS
#################

wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/HUMAN/goa_human.gaf.gz
OUTFILE=GO.goa_human_`date "+%Y.%m.%d"`.gz
mv goa_human.gaf.gz $OUTFILE

wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/MOUSE/goa_mouse.gaf.gz
OUTFILE=GO.goa_mouse_`date "+%Y.%m.%d"`.gz
mv goa_mouse.gaf.gz $OUTFILE
# gunzip -k $OUTFILE

wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/FLY/goa_fly.gaf.gz
OUTFILE=GO.goa_fly_`date "+%Y.%m.%d"`.gz
mv goa_fly.gaf.gz $OUTFILE
# gunzip -k $OUTFILE

wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/ARABIDOPSIS/goa_arabidopsis.gaf.gz
OUTFILE=GO.goa_arabidopsis_`date "+%Y.%m.%d"`.gz
mv goa_arabidopsis.gaf.gz $OUTFILE
# gunzip -k $OUTFILE

wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/RAT/goa_rat.gaf.gz
OUTFILE=GO.goa_rat_`date "+%Y.%m.%d"`.gz
mv goa_rat.gaf.gz $OUTFILE
# gunzip -k $OUTFILE

wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/WORM/goa_worm.gaf.gz
OUTFILE=GO.goa_worm_`date "+%Y.%m.%d"`.gz
mv goa_worm.gaf.gz $OUTFILE
# gunzip -k $OUTFILE

wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/ZEBRAFISH/goa_zebrafish.gaf.gz
OUTFILE=GO.goa_zebrafish_`date "+%Y.%m.%d"`.gz
mv goa_zebrafish.gaf.gz $OUTFILE
# gunzip -k $OUTFILE



mv GO.* ../ACs
