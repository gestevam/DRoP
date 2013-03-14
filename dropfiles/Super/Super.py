#!/usr/bin/python
#*********************************************************************************
# preDRoP.py
# Feb. 26, 2011
# Bradley Kearney
# Processes pdb files for DRoP analysis.
#*********************************************************************************

import sys
import time
import webbrowser
import os
import urllib
import shutil

def run():
    argv = sys.argv[1:]
    try:
        id=argv[0]
    except:
        return

    root =  'Renumbered/'
    if(root[-1:] != '/'):
        root += '/'
    url = 'http://129.10.89.145/running.php?job=%d&status=300'%int(id)
    print url
    raw_return=urllib.urlopen(url).read()
    pdb_filenames = []
    filenames = os.listdir(os.getcwd())
    for f in filenames:
        if(f[-4:] == '.pdb'):
            pdb_filenames.append(f)
    basis=pdb_filenames[0]
    shutil.copyfile(basis,'../Final/'+basis)
    for f in pdb_filenames:
        if (f!=basis):
	    os.system("python cealign.py %s %s"%(basis,f))
	    
    url = 'http://129.10.89.145/running.php?job=%d&status=399'%int(id)
    raw_return=urllib.urlopen(url).read()
    os.chdir('../Final')
    os.system("python DRoP.py "+id)
    return
if(__name__ == '__main__'):
    run()
        
        
