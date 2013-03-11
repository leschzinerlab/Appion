#!/usr/bin/env python

#Inputs
pwd = '/labdata/allab/michaelc/David_Dicer_data'
base = '12aug01q_'
outfile = 'dicer_upload.txt'
pixelsize = 2.18e-10	#IN METERS
tiltangle = 55
binning = 1
magnification = 50000
hightension = 120
defocus = -1e-06		#IN METERS
#####################

o1 = open(outfile,'w')

#filenamepath	pixelsize(meters)	binx	biny	nominalscopemag	df	HT	alphatilt

first=1
last=35

while first <= last:

	tilt ='%s/%s%03dt.mrc' %(pwd,base,first)
	untilt = '%s/%s%03du.mrc' %(pwd,base,first)

	o1.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(untilt,str(pixelsize),str(binning),str(binning),str(magnification),str(defocus),str(hightension),str(0)))

	o1.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(tilt,str(pixelsize),str(binning),str(binning),str(magnification),str(defocus),str(hightension),str(tiltangle)))	
	first = first + 1

