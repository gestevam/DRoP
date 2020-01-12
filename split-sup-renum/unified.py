import SplitChains, lsqman, RenumberWaters
import sys, os, re

def mkdir(path):
	if(not os.path.exists(path)):
		os.popen('mkdir %s' % path)
		return True
	return False
def rmdir(path):
	if(os.path.exists(path)):
		os.popen('rm %s/*' % path)
		os.popen('rmdir %s' % path)
		return True
	return False

def next_command(prompt):
	input = re.split('\s*', raw_input(prompt))
	try:
		if(input[0]==''): del input[0]
		if(input[-1] == ''): del input[-1]
		return (input[0], input[1:])
	except:
		return ('',[])

class main:
	def __init__(self, argv):
		self.logfile = open('PDBTool.log', 'w')
		self.log("""
Welcome to PDBTool, where you can split files by chain,
superimpose chains, and renumber waters according to concensus,
all in one place.
""")
		self.log("""
Commmands:
split:     splits specified chains; can also specify cutoff (default 5.0 A); superimposes the resulting molecules
super:     superimposes files
renum:     gives analogous waters in the different files the same res num; can also specify initial cutoff (default 1.4 A)
#""")
		self.reset_files()


		while(True):
			cmd, args = next_command('     >>> ')
			if(cmd == 'quit'):
				break
			if(cmd == 'split'):
				chains = []
				cutoff = 5.
				for arg in args:
					try:
						cutoff = float(arg)
					except:
						chains.append(arg)
				self.split(chains, cutoff)
				continue
			if(cmd == 'super'):
				self.super()
				continue
			if(cmd == 'renum'):
				try:
					start_err = float(args[0])
				except:
					start_err = 1.4
				self.renum(start_err)
				break
			print "%$#@!"
			

	def reset_files(self):
		files = filter(lambda x: x[-4:]=='.pdb', os.listdir(os.getcwd()))
		files.sort()
		self.pdb_files = files
		self.log("\n          Current Directory: %s\n          Using PDB files in current directory:\n" % os.getcwd())
		for i,file in enumerate(files):
			self.log("          %3d  %s\n" % (i, file))
	def log(self, str):
		print str,
		self.logfile.write(str)
		
	def split(self, chain_names, cutoff):
		mkdir('split')
		if(not chain_names):
			print 'Which chains would you like to split?'
			chain_names = [chain_name.strip() for chain_name in re.split('\s*,?\s*', raw_input('split>>> '))]
		self.splitters = [SplitChains.Splitter(file) for file in self.pdb_files]
		try:
			for s in self.splitters:
				self.log("splitting file %s\n" % s.pdb.filename)
				s.cutoff = cutoff
				s.split(chain_names)
		except KeyError:
			print "Those chains aren't working for me"
			rmdir('split')
		finally:
			os.chdir('split')
			self.reset_files()
			self.super()
	def super(self):
		print 'superimposing files'
		mkdir('super')
		lsqman.run_lsqman(self.pdb_files)
		os.chdir('super')
		self.reset_files()
	def renum(self, start_err):
		root = 'renum/'
		mkdir('renum')
		a = RenumberWaters.Analyzer(self.pdb_files, root, err=start_err)
		print "          Hit return until you like the way it looks, then quit. Instead of hitting return, you can also type a maximum acceptable error value. To see the log file again, type 'view'."
		while(True):
			arg = raw_input('renum>>> ').strip()
			if(arg == 'quit'):
				break
			if(arg == 'view'):
				os.popen('konqueror %s/master.html' % root)
				continue
			if(arg == ''):
				max_err = None
			else:
				try:
					max_err = float(arg)
					if(max_err < a.err):
						print 'already there, mate'
						continue
				except:
					print "%$#@!"
					continue
			a.group_waters(max_err)
			a.write()
			os.popen('konqueror %s/master.html' % root)
if __name__=='__main__':
	main(sys.argv)