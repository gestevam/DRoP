#!/usr/bin/python
#*********************************************************************************
# preDRoP.py
# Feb. 26, 2011
# Bradley Kearney
# Processes pdb files for DRoP analysis.
#*********************************************************************************

from math import *
import sys
import os
import copy
import zipfile as zipf
import shutil

def run():
    os.system("/usr/bin/python cealign.py ND01PRESUPER.pdb ND02PRESUPER.pdb")
    return
    #print "Preprocessing files. Please wait."
    argv = sys.argv[1:]
    try:
        writedirectory=argv[0]
    except:
        print "There's something really wrong. Aborting."
        return
    filenames = os.listdir(os.getcwd())
    #if(not os.path.exists('./upload/'+writedirectory)):
        #os.makedirs(writedirectory)
    filenames=os.listdir(os.getcwd())
    for f in filenames:
        if f[-3:]=='.py' or f=="config.txt":
            shutil.copyfile(f,'./upload/'+writedirectory+'/'+f)
    os.chdir('./upload/'+writedirectory)
    #os.system("python unziptest.py")
    filenames = os.listdir(os.getcwd())
    for f in filenames:
        if(f[-4:] == '.zip'):
            myfile=zipf.ZipFile(f)
            for name in myfile.namelist():
                if name[-4:] == ".pdb":
                    data=myfile.read(name)
                    if not os.path.exists('OriginalFiles/'):
                        os.makedirs('OriginalFiles/')
                    if not os.path.exists('Preprocess/'):
                        os.makedirs('Preprocess/')
                    out_filename=name.split("/")[-1]
                    file=open('OriginalFiles/'+out_filename, 'w')
                    file.write(data)
                    file.close()
                    file=open('Preprocess/'+out_filename,'w')
                    file.write(data)
                    file.close()
            #pdb_filenames.append(f)
    print "everything is fine"
    return
    a = Analyzer(pdb_filenames, root, err=start_err)
    input = ''
    a.phase3()
    a.viewgraph()
    return
if(__name__ == '__main__'):
    run()
        
        
