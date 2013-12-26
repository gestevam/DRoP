import RenumberWaters, SplitChains, lsqman
import os, re, sys

print "Parameters for split"
chains = raw_input("What chains? (default: A, B)\n ")
chains = [name.strip() for name in re.split('\s*,?\s*', chains)]
if(not chains or not chains[0]):
	chains = ['A','B']
cutoff = raw_input("What cutoff? (default: 5.0)\n ").strip()
if not cutoff:
	cutoff = 5.0
else:
	cutoff = float(cutoff)
	
print "Parameters for renum"
max_err = raw_input("What cutoff for water renumbering? (default: 1.4)\n ")
if(not max_err):
	max_err = 1.4
else:
	max_err = float(max_err)

def mkdir(path):
	if(not os.path.exists(path)):
		os.popen('mkdir %s' % path)
		return True
	return False
def get_files():
	files = filter(lambda x: x[-4:]=='.pdb', os.listdir(os.getcwd()))
	files.sort()
	return files

print "*"*10 + "split" + "*"*10
print "Chains: %s   Cutoff: %.1f" % (" and ".join(chains), cutoff)
files = get_files()
splitters = [SplitChains.Splitter(file) for file in files]
for i,s in enumerate(splitters):
	s.cutoff = cutoff
	s.split(chains)
	print 'splitting %3.0f%% complete' % ((i+1.)*100./len(splitters))
os.chdir('split')

print "*"*10 + "super" + "*"*10
files = get_files()
lsqman.run_lsqman(files)
os.chdir('super')

print "*"*10 + "renum" + "*"*10

files = get_files()
mkdir('renum')
a = RenumberWaters.Analyzer(files, 'renum/',err=1.4)
a.group_waters(max_err)
a.write()
os.popen('konqueror renum/master.html')
