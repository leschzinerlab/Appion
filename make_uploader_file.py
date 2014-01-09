#!/usr/bin/env python

#This script will generate a text file containing a list of untilted and tilted micrographs for uploading into Appion. 
#The output file will have the following columns: 

#/path/to/filename	pixelsize(meters)	binx	biny	nominalscopemag	df	HT	alphatilt

#And the micrographs will be listed in the following order:

#micrograph1_untilted
#micrograph1_tilted
#micrograph2_untilted
#micrograph2_tilted
#etc.

#################
#INPUTS ARE HERE#
#################

#NOTE: Assumes linear ordering of micrographs

pwd = '/labdata/allab/michaelc/David_Dicer_data'	#Full path to micrographs
base = '12aug01q_'					#Basename of micrographs. Leave blank if no basename.
outfile = 'dicer_upload.txt'				#Output filename
pixelsize = 2.18e-10					#Pixel size (IN METERS)	
tiltangle = 55						#Tilt angle used 
binning = 1						#Binning of micrographs (1 = no binning)
magnification = 50000					#Magnification
hightension = 120					#High tension of microscope (IN KILOVOLTS)
defocus = -1e-06					#Approx. defocus (IN METERS)	
tot = 35						#Total number of tilt pairs 

#################
#Program ########
#################

o1 = open(outfile,'w')

first=1
last=tot

while first <= last:

	tilt ='%s/%s%03dt.mrc' %(pwd,base,first)
	untilt = '%s/%s%03du.mrc' %(pwd,base,first)

	o1.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(untilt,str(pixelsize),str(binning),str(binning),str(magnification),str(defocus),str(hightension),str(0)))

	o1.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(tilt,str(pixelsize),str(binning),str(binning),str(magnification),str(defocus),str(hightension),str(tiltangle)))	
	first = first + 1

