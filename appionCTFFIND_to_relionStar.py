#!/usr/bin/env python 


import optparse
from sys import *
import os,sys,re
from optparse import OptionParser
import glob
import subprocess
from os import system
import linecache
import time


#=========================
def setupParserOptions():
        parser = optparse.OptionParser()
        parser.set_usage("%prog -i <ctf from appion> --path=<path to micros> --appion=<appion base name to remove> --cs=<cs> --kev=<kev> ")
        parser.add_option("-i",dest="ctf",type="string",metavar="FILE",
                help="CTF downloaded file from Appion CTF summary page")
	parser.add_option("--path",dest="folder",type="string",metavar="STRING",
                help="Relative path to micrographs that Relion will use (e.g. 'Micrographs')")
	parser.add_option("--appion",dest="appion",type="string",metavar="STRING",
                help="Appion base name to remove (E.g. Remove '14jul22y_' from '14jul22y_Jul15_18.09.54.box")
	parser.add_option("--cs",dest="cs",type="float",metavar="FLOAT",
                help="Spherical aberration (Cs) of microscope (mm)")
	parser.add_option("--kev",dest="kev",type="int",metavar="INT",
                help="Accelerating voltage of microscope (keV)")
        parser.add_option("--pixel",dest="detector",type="float",metavar="float",
                help="Pixel size of detector (um) (K2 = 14 um)")
	parser.add_option("--mag",dest="mag",type="int",metavar="INT",
                help="Nominal magnification of microscope")
	parser.add_option("-d", action="store_true",dest="debug",default=False,
                help="debug")
        options,args = parser.parse_args()

        if len(args) > 0:
                parser.error("Unknown commandline options: " +str(args))

        if len(sys.argv) < 2:
                parser.print_help()
                sys.exit()
        params={}
        for i in parser.option_list:
                if isinstance(i.dest,str):
                        params[i.dest] = getattr(options,i.dest)
        return params

#=============================
def checkConflicts(params):
        if not os.path.exists(params['ctf']):
                print "\nError: CTF file '%s' does not exist\n" % params['CTF']
                sys.exit()

        if os.path.exists('all_micrographs_ctf.star'):
                print "\nError: all_micrograhps_ctf.star already exists, exiting.\n"
                sys.exit()

#===============================
def convertAppionToRelionCTF(params):

	relionOut = writeRelionHeader()

	out = open('all_micrographs_ctf.star','w')

	ctf = open(params['ctf'],'r')

	for line in ctf:
		l = line.split()
		
		if l[0] == 'image':
			continue
		
		#Prepare micrograph name
		micro = re.sub('%s' %(params['appion']),'',l[11])
		microname = '%s/' %(params['folder'])+micro+'.mrc'
		if params['debug'] is True:
			print microname
	
		#Get defocus information
		df1 = l[2].split('e')
		df1 = float(df1[0])*10000
		
		df2 = l[3].split('e')
		df2 = float(df2[0])*10000
		astig = float(l[4])
		ampcontrast = float(l[5])
		crosscorr = float(l[10])
		
		relionOut+='%s  %.6f  %.6f  %.6f  %.6f  %.6f  %.6f  %.6g  %.6f  %.6f\n' %(microname,df1,df2,astig,params['kev'],params['cs'],ampcontrast,params['mag'],params['detector'],crosscorr)
 
	out.write(relionOut)

#================================
def writeRelionHeader():

	relion='\n'
	relion+='data_\n'
	relion+='\n'
	relion+='loop_\n'
	relion+='_rlnMicrographName #1\n'
	relion+='_rlnDefocusU #2\n'
	relion+='_rlnDefocusV #3\n'
	relion+='_rlnDefocusAngle #4\n'
	relion+='_rlnVoltage #5\n'
	relion+='_rlnSphericalAberration #6\n' 
	relion+='_rlnAmplitudeContrast #7\n'
	relion+='_rlnMagnification #8\n'
	relion+='_rlnDetectorPixelSize #9\n'
	relion+='_rlnCtfFigureOfMerit #10\n' 

	return relion

#==============================
if __name__ == "__main__":

        params=setupParserOptions()
        checkConflicts(params)
	convertAppionToRelionCTF(params)
