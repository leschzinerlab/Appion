#!/usr/bin/env python

#This script will generate a text file containing a list of untilted and tilted micrographs for uploading into Appion. 
#NOTE: Assumes linear ordering of micrographs and numbering: basename01_00.mrc, where there are two digits for micrograph number ('01').

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

pwd = '/labdata/allab/michaelc/5merRCT/gHgLgO'	#Full path to micrographs
base = ''					#Basename of micrographs. Leave blank if no basename.
outfile = 'RCT_upload.txt'				#Output filename
pixelsize = 2.16e-10					#Pixel size (IN METERS)	
tiltangle = -50						#Tilt angle used 
binning = 1						#Binning of micrographs (1 = no binning)
magnification = 50000					#Magnification
hightension = 120					#High tension of microscope (IN KILOVOLTS)
defocus = -1e-06					#Approx. defocus (IN METERS)	
tot = 30						#Total number of tilt pairs 
untilt_extension = '_00'				#Indicator in filename specifying if micrograph was tilted
tilt_extension = '_50'					#Indicator in filename specifying if micrograph was tilted

#################
#Program ########
#################

o1 = open(outfile,'w')

first=1
last=tot


while first <= last:

	tilt ='%s/%s%02d%s.mrc' %(pwd,base,first,tilt_extension)
	untilt = '%s/%s%02d%s.mrc' %(pwd,base,first,untilt_extension)

	o1.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(untilt,str(pixelsize),str(binning),str(binning),str(magnification),str(defocus),str(hightension),str(0)))

	o1.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(tilt,str(pixelsize),str(binning),str(binning),str(magnification),str(defocus),str(hightension),str(tiltangle)))	
	first = first + 1

