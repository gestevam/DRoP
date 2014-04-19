#!/usr/bin/python
#*********************************************************************************
# preDRoP.py
# Feb. 26, 2011
# Bradley Kearney
# Processes pdb files for DRoP analysis.
#*********************************************************************************

import sys
import os
import copy
import zipfile as zipf
import shutil
82
def run():
    argv = sys.argv[1:]
    try:
        writedirectory=argv[0]
    except:
        print "There's something really wrong. Aborting."
        return
    print writedirectory
    filenames = os.listdir(os.getcwd())
    if(not os.path.exists('./upload/'+writedirectory)):
        os.makedirs('./upload/'+writedirectory)
    if(not os.path.exists('./upload/'+writedirectory+'/Final')):
        os.makedirs('./upload/'+writedirectory+'/Final')
    os.chdir('./dropfiles/Preprocess')
    filenames=os.listdir(os.getcwd())
    os.chdir('../Final')
    filenames=os.listdir(os.getcwd())
    for f in filenames:
        if f[-3:]=='.py' or f=="config.txt":
            shutil.copyfile(f,'../../upload/'+writedirectory+'/Final/'+f)
    os.chdir('../../upload/'+writedirectory)
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
                    if not os.path.exists('Final/'):
                        os.makedirs('Final/')
                    out_filename=name.split("/")[-1]
                    file=open('OriginalFiles/'+out_filename, 'w')
                    file.write(data)
                    file.close()
                    file=open('Final/'+out_filename,'w')
                    file.write(data)
                    file.close()
            #pdb_filenames.append(f)
    print "everything is fine"
    os.chdir('Final')
   
    print os.getcwd()
    print "going into round 2."
    os.system("python DRoP.py "+writedirectory)
    return
if(__name__ == '__main__'):
    run()
        
        
