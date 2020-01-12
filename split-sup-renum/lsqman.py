import os,sys
from pdb import *

def run_lsqman(files):
	base = files[0]
	if(not os.path.exists('super')):
		os.popen("mkdir super")
	
	max_res_num = 0
	base_pdb = PDB(base)
	for atom in base_pdb:
		if(atom['type'] in atom_names and atom['res name'] not in water_names):
			max_res_num = max(max_res_num, atom['res num'])
	
	log=''
	
	for file in files:
		log += os.popen4("""echo '
re m1 %(base)s
re m2 %(file)s
at ex
ex m1
a1-%(max_res_num)d
m2
a1-%(max_res_num)d
apply m1 m2
wr m2 super/%(file)s
quit' | /usr/local/dejavu/lx_lsqman""" % locals())[1].read()
	
	open('lsqman.log', 'w').write(log)

if(__name__=='__main__'):
	files = filter(lambda x: x[-4:]=='.pdb', os.listdir(os.getcwd()))
	run_lsqman(files)