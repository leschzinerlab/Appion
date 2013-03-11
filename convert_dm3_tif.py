#!/usr/bin/env python

import glob
import subprocess

files = glob.glob('*.dm3')

for im in files:

	cmd = 'proc2d %s %s.mrc mrc' %(im,im[:-4])
	subprocess.Popen(cmd,shell=True).wait()
	
