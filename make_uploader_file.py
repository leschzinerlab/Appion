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
        parser.set_usage("%prog -p <path/to/images> --tilt=[tiltangle] --apix=[pixelsize] --mag=[magnification] --HT=[hightension] --def=[defocus] --Uext=[untiltExtension] --Text=[tiltExtension]")
        parser.add_option("-p",dest="path",type="string",metavar="FILE",
                help="Absolute path to the folder containing tilt-mates")
        parser.add_option("--untilt",dest="untilt",type="int", metavar="INT",default=0,
                help="Tilt angle for untilted particles")
	parser.add_option("--tilt",dest="tilt",type="int", metavar="INT",
                help="Tilt angle for tilted particles")
        parser.add_option("--apix",dest="apix",type="float", metavar="FLOAT",
                help="Pixel size (A/pix)")
        parser.add_option("--mag",dest="mag",type="float", metavar="FLOAT",
                help="Magnification")
	parser.add_option("--HT",dest="HT",type="int", metavar="INT",
                help="High tension of microscope (keV)")
	parser.add_option("--def",dest="def",type="float", metavar="FLOAT",
                help="Defocus (approx.) of images (um)")
	parser.add_option("--Uext",dest="Uext",type="string", metavar="STRING",
                help="Untilted micrograph extension (e.g. '00', 'u')")
	parser.add_option("--Text",dest="Text",type="string", metavar="STRING",
                help="Tilted micrograph extension (e.g. '01', 't')")
        parser.add_option("--leginon",action="store_true",dest="leginon",default=False,
		help="Flag if tilt mates came from leginon")
	parser.add_option("-d", action="store_true",dest="debug",default=False,
                help="debug")
        options,args = parser.parse_args()

        if len(args) > 1:
                parser.error("Unknown commandline options: " +str(args))

        if len(sys.argv) < 5:
                parser.print_help()
                sys.exit()
        params={}
        for i in parser.option_list:
                if isinstance(i.dest,str):
                        params[i.dest] = getattr(options,i.dest)
        return params
#=============================
def checkConflicts(params):
        if not params['path']:
                print "\nWarning: no path specified\n"
        elif not os.path.exists(params['path']):
                print "\nError: path '%s' does not exist\n" % params['path']
                sys.exit()
        if not params['tilt']:
                print "\nWarning: no tilt angle specified for tilted particles\n"
                sys.exit()
        if not params['apix']:
                print "\nWarning: no pixel size specified\n"
                sys.exit()
	if not params['mag']:
                print "\nWarning: no magnification specified\n"
                sys.exit()
	if not params['HT']:
                print "\nWarning: no high tension specified\n"
                sys.exit()
	if not params['def']:
                print "\nWarning: no defocus specified\n"
                sys.exit()
	if not params['Text']:
                print "\nWarning: no tilted micrograph extension specified\n"
                sys.exit()
	if not params['Uext']:
                print "\nWarning: no untilted micrograph extension specified\n"
                sys.exit()

#==================
def start(param):
	
	o1 = open('RCT_upload.txt','w')	#output file

	first=1
	#Number of untilted micrographs:
	numUntilt = len(glob.glob('%s/*%s.mrc' %(param['path'],param['Uext'])))
	if param['debug'] is True:
		print 'Number of untilted micrographs = %i' %(numUntilt)
	#Number of tilted micrographs: 
	numTilt = len(glob.glob('%s/*%s.mrc' %(param['path'],param['Text'])))
        if param['debug'] is True:
                print 'Number of tilted micrographs = %i' %(numTilt)
	if numTilt != numUntilt: 
		print 'Warning: Number of untilted and tilted micrographs are unequal. Check output file to confirm they are correctly matched!'
	totalMicros = numTilt + numUntilt
	
	tiltedList = glob.glob('%s/*%s.mrc' %(param['path'],param['Text']))
	
	for tilt in sorted(tiltedList):

		tiltOrig = tilt
	
		if params['leginon'] is True:
                        #parse this type of filename: 14jul09b_00009hl_00_00008en_00.mrc 
                        tiltsplit=tilt.split('hl')
                        if params['debug'] is True:
                                print tiltsplit
                        
			untiltMiddleChange = '_'+param['Uext'][-2:]+'_'+tiltsplit[1][4:]
	
                        tilt=tiltsplit[0]+'hl'+untiltMiddleChange

			if params['debug'] is True:
				print tilt

		#Retrieve untilted micrograph pair filename	
		tiltNoExt = tilt.split('%s'%(param['Text']+'.'))
		if params['debug'] is True:
			print tiltNoExt
		
		numPartsTilt = len(tiltNoExt)
		i = 0
		untilt = ''
		while i < numPartsTilt-1:
			if i == 0:
				untilt = untilt+tiltNoExt[i]	
				i = i + 1
				continue
			untilt = untilt+tiltNoExt[i]
			if params['debug'] is True:
				print untilt
			i = i + 1
	
		#Check that tilt mates exist
		if os.path.exists('%s' %(untilt+'%s.mrc'%(param['Uext']))) is False:
			if params['debug'] is True:
				print '%s' %(untilt+'%s.mrc'%(param['Uext']))
			print 'No tilt mate for %s' %(tilt)
			continue		

		o1.write('%s\t%s\t1\t1\t%i\t%s\t%s\t%s\n' %(untilt+'%s.mrc'%(param['Uext']),str(param['apix'])+'e-10',param['mag'],str(param['def'])+'e-06',str(param['HT']*1000),param['untilt']))

		o1.write('%s\t%s\t1\t1\t%i\t%s\t%s\t%s\n' %(tiltOrig,str(param['apix'])+'e-10',param['mag'],str(param['def'])+'e-06',str(param['HT']*1000),str(param['tilt'])))


#==============================
if __name__ == "__main__":

        params=setupParserOptions()
        checkConflicts(params)
        start(params)

