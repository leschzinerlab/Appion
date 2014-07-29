#!/usr/bin/env python 

import shutil
import optparse
from sys import *
import os,sys,re
from optparse import OptionParser
import glob
import subprocess
from os import system
import linecache
import time
import re

#=========================
def setupParserOptions():
        parser = optparse.OptionParser()
        parser.set_usage("%prog --appion=<appion basename to remove> --path=<path to box files> --output<output path>")
        parser.add_option("--appion",dest="appion",type="string",metavar="STRING",
                help="Appion basename to remove (E.g. Remove '14jul22y_' from '14jul22y_Jul15_18.09.54.box'")
        parser.add_option("--path",dest="path",type="string",metavar="STRING",
                help="Path to box files")
        parser.add_option("--output",dest="output",type="string", metavar="STRING",
                help="Output path for renamed box files")
        parser.add_option("-d", action="store_true",dest="debug",default=False,
                help="debug")
        options,args = parser.parse_args()

        if len(args) > 0:
                parser.error("Unknown commandline options: " +str(args))

        if len(sys.argv) < 3:
                parser.print_help()
                sys.exit()
        params={}
        for i in parser.option_list:
                if isinstance(i.dest,str):
                        params[i.dest] = getattr(options,i.dest)
        return params

#=============================
def checkConflicts(params):
        if not os.path.exists(params['path']):
                print "\nError: Path '%s' does not exist\n" % params['path']
                sys.exit()
	if not os.path.exists(params['output']):
                print "\nError: Output path '%s' does not exist\n" % params['output']
                sys.exit()

#==============================
def renameBoxFiles(params):
	
	boxlist = glob.glob('%s/*.box' %(params['path']))

	for box in boxlist:
	
		boxline = box.split('/')
		box1 = boxline[-1]	

		newbox = re.sub('%s' %(params['appion']),'',box1)
		
		if params['debug'] is True:
			print "\nCoping %s to %s/%s\n" %(box,params['output'],newbox)

		shutil.copyfile('%s' %(box),'%s/%s' %(params['output'],newbox))

#==============================
if __name__ == "__main__":

        params=setupParserOptions()
        checkConflicts(params)
	renameBoxFiles(params)
