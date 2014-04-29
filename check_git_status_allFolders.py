#!/usr/bin/env python

import optparse
from sys import *
import os,sys,re
from optparse import OptionParser
import glob
import subprocess
from os import system


#=========================
def setupParserOptions():
        parser = optparse.OptionParser()
        parser.set_usage("%prog --run")
	parser.add_option("--run", action="store_true",dest="run",default=False,
                help="Run program and check git status on all folders in current directory")
	parser.add_option("--verbose", action="store_true",dest="verbose",default=False,
                help="Print to terminal verbose output")
	options,args = parser.parse_args()
        if len(args) > 0:
                parser.error("Unknown commandline options: " +str(args))
	if len(sys.argv) == 1:
                parser.print_help()
                sys.exit()
        params={}
        for i in parser.option_list:
                if isinstance(i.dest,str):
                        params[i.dest] = getattr(options,i.dest)
	return params


#==============================
if __name__ == "__main__":

	params=setupParserOptions()
	
	if params['verbose'] is True:
		print '\n'
		print 'This program will check the git status on each folder in current working'
		print 'directory and print it to the terminal'
		print '\n'

	if params['run'] is True:
		folders = glob.glob('*')
		for folder in folders:
			if folder[:5] == 'check':
				continue	
			if params['verbose'] is True:
				print 'Checking status of repo %s....' %(folder)
			os.chdir(folder)
			if os.path.exists('.git') is False:
				if params['verbose'] is True:
					print '   --> Folder %s is not a git repo' %(folder)
				os.chdir('..')
				continue
			gitstatus = subprocess.Popen("git status", shell=True, stdout=subprocess.PIPE).stdout.read().strip()
			git = gitstatus.split()
			if git[5] == 'Changed':
				print '   --> There are uncommitted changes in repo %s' %(folder)
			if git[5] == 'Untracked':
				print '   --> There are uncommitted changes in repo %s' %(folder)
			os.chdir('..')
	
	if params['run'] is False:
		print 'Exiting, please specify --run to check git status on folders'
		sys.exit()

