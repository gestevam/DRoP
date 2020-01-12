#!/usr/bin/python

#*********************************************************************************
# RenumberWaters.py
# Created July 1, 2008 by Daniel M. Roberts
# This program lets you automatically renumber waters with a
# some (limited) interactivity.
#
# When calling this script you may specify a group of PDB files
# to be compared and renumbered (default: '*.pdb'); you may specify
# a directory in which to put the renumbered PDB files and the log file
# (default: 'Renumbered/') following '-r'; and you may specify an initial
# acceptable error (in angstroms) (default: 1.4) following '-e'.
#
# Once you have called the script, there are two commands which you may run:
# 'group' and 'view'. 'group' automatically groups waters, and 'view' shows
# the log file, which is in html format. After viewing the log, you can
# assess whether to raise the acceptable error in order to find more matches.
# To do this, type 'group 1.7' for example. This will run the regrouping
# algorithm in a cycle, incrementing the acceptable error by .05 A until
# it reaches the number you specified.
#
# To exit the program, type 'quit'. This will also save any changes you
# have made.
#*********************************************************************************

import re, sys, os, random
from pdb import *
def shell(cmd):
	return os.popen4(cmd)[1].read()[:-1]

class Cluster(list):
	def __init__(self, atom):
		list.__init__(self)
		self.sum = [0.]*3
		self.res_num = None
		#self.a4p = {}
		self.append(atom)
	def append(self,atom):
		list.append(self, atom)
		#self.a4p[atom.pdb.number]=atom
		atom.cluster = self
		self.sum = [self.sum[i]+atom.position()[i] for i in range(3)]
		self.reset_calculated_values()
	def remove(self, atom):
		list.remove(self, atom)
		#del self.a4p[atom.pdb.number]
		atom.cluster = None
		self.sum = [self.sum[i]-atom.position()[i] for i in range(3)]
		self.reset_calculated_values()
	def reset_calculated_values(self):
		self._mean = self._sd = None
	def atom_for_pdb(self, i):
		for atom in self:
			if atom.pdb.number == i:
				return atom
		"""try:
			return self.a4p[i]
		except:
			return None"""
	def renumber(self, res_num):
		self.res_num = res_num
		for atom in self:
			atom['res num'] = res_num
	def mean(self):
		if(self._mean): return self._mean
		l = len(self)
		self._mean = [coor/l for coor in self.sum]
		return self._mean
	def std_dev(self):
		if(self._sd): return self._sd
		mean = self.mean()
		sd = sum([sum([(mean[i]-atom.position()[i])**2 for i in range(3)]) for atom in self])
		try:
			sd /= len(self)-1
		except:
			return Infinity
		self._sd = sd**.5
		return self._sd
	def rmsd_str(self, na='N/A'):
		v = self.std_dev()
		if(v==Infinity): return na
		else: return "%.3f" % v
	def estimate_fit(self, atom, err):
		if atom.cluster == self:
			return atom.distance_from(self.mean(), err*(1.+1./len(self)))
		else:
			return atom.distance_from(self.mean(), err)
		
		
	def cmp(self, rhs):
		self_len, rhs_len = len(self), len(rhs)
		if(self_len == rhs_len):
			if(self_len == 1):
				return cmp(self[0].pdb.number, rhs[0].pdb.number)
			return cmp(self.std_dev(), rhs.std_dev())
		else: return -cmp(self_len, rhs_len)

class Analyzer:
	increment = .05
	class Cluster_List(list):
		def move(self, atom, cluster):
			if(id(atom.cluster) == id(cluster) or not cluster):
				raise Exception
			if(atom.cluster):
				old_cluster = atom.cluster
				old_cluster.remove(atom)
				if(len(old_cluster)==0):
					self.remove(old_cluster)
			cluster.append(atom)
		def isolate(self, atom):
			if(not atom.cluster):
				raise Exception
			old_cluster = atom.cluster
			old_cluster.remove(atom)
			if(not old_cluster):
				self.remove(old_cluster)
			self.append(Cluster(atom))
			

	def __init__(self, pdb_filenames, root, err=1.4):
		self.pdbs = []
		for filename in pdb_filenames:
			self.pdbs.append(PDB(filename, root + filename.split('/')[-1]))
		#self.pdbs.sort(key=PDB.__str__)
		self.pdbs.sort(key=str)
		for i,pdb in enumerate(self.pdbs):
			pdb.number = i
			pdb.shortname = pdb.filename.split('/')[-1]
		self.waters = []
		for pdb in self.pdbs:
			for atom in pdb:
				if(atom['res name'] in water_names):
					self.waters.append(atom)
		self.root = root
		self.master = Analyzer.Cluster_List()
		self.master_path = root + 'master.html'
		self.err = self.start_err = err
	def run(self):
		self.group_waters()
		self.write()
		
	def group_waters(self, max_err=None):
		if(not max_err):
			max_err = self.err
		def place_water(atom):
			"""
			Places atom in the most appropriate cluster; returns True for change made, False for no changes made
			"""
			best_value = 2*self.err
			best_cluster = None
			for cluster in self.master:
				fit = cluster.estimate_fit(atom, self.err)
				if(fit):
					if(fit < best_value):
						competitor = cluster.atom_for_pdb(atom.pdb.number)
						if(competitor and competitor != atom):
							continue
						best_value, best_cluster = (fit, cluster)
					break
			if(best_cluster):			#if a match was found
				if(id(best_cluster) != id(atom.cluster)):	# and it's not the one atom is already in
					self.master.move(atom, best_cluster)	# then move it there
				else:
					return False # no change made
			else:					#if NO match was found
				if(not atom.cluster):		#and there was never a match before
					self.master.append(Cluster(atom)) #then make a new cluster
				else:				#but if there was a match before
					self.master.isolate(atom)	#take it out and put it in its own cluster
			return True	# a change was made
		
		random.shuffle(self.waters)
		while(self.err <= max_err+.001):
			changes_made = 0;
			print 'Grouping waters (err=%4.2f)' % (self.err)
			for water in self.waters:
				if(place_water(water)):
					changes_made += 1
			self.master.sort(Cluster.cmp)
			if(not changes_made):
				print 'Waters grouped into %d groups' % len(self.master)
				self.err += .05
				
		
		if(sum([len(cluster) for cluster in self.master]) != len(self.waters)):
			print 'Houston we have a problem!'
			print 'Now %d atoms, were %d' % (sum([len(cluster) for cluster in self.master]), len(self.waters))
			"""for atom in self.waters:
				count = 0
				for cluster in self.master:
					for atom2 in cluster:
						if(atom == atom2): count+=1
				if count == 0: print "WATER NOT LISTED:\n%s" % atom
				if count > 1: print "WATER LISTED MULTIPLE TIMES:\n%s" % atom"""
				
			
	def write(self):
		self.master.sort(Cluster.cmp)
		self.renumber_clusters()
		for pdb in self.pdbs:
			pdb.write()
		self.write_master()
	def write_master(self):
		print "writing master file..."
		user = shell('echo $USER')
		date = shell('date')
		file = open(self.master_path, 'w')
		n_pdbs = len(self.pdbs)
		for cluster in self.master:
			cluster.pdbs = [atom.pdb for atom in cluster]
		
		#for pdb_name in pdb_names:
		#	file.write("%s\n" % pdb_name)
		
		#file.write("\n")
		#for cluster in self.master:
			#for atom in cluster:
				#file.write("%s:%s " % (atom.pdb.number, atom.line_number))
			#file.write("\n")
		file.write("""
		<html>
		<head>
		<title>Water Concensus List</title>
		<style>
		table {
			border-collapse: collapse;
		}
		th {
			text-align: center;
		}
		th.res_num {
			text-align: left;
		}
		td.res_num {
			width: 40px;
			text-align: left;
		}
		tr.cluster {
			background-color: lightskyblue;
			border: thin solid royalblue;
		}
		tr.cluster:hover {
			background-color: white;
		}
		th.file_n {
			text-align: center;
			color: limegreen;
		}
		td.file_n {
			width: 20px;
			text-align: right;
			color: limegreen;
		}
		th.n_files {
			color: black;
		}
		td.n_files {
			width: 25px;
			text-align: right;
			color: black;
		}
		th.coor {
			text-align: center;
			color: blue;
		}
		td.coor {
			width: 60px;
			font-family: courier;
			font-size: 12;
			text-align: right;
			color: blue;
		}
		th.rmsd {
			text-align: center;
			color: red;
		}
		td.rmsd {
			width: 60px;
			font-family: courier;
			font-size: 12;
			text-align: right;
			color: red;
		}
		th.filename {
			text-align: left;
			color: green;
		}
		td.filename {
			font-family: Times New Roman;
			font-size: 12;
			color: green;
		}
		</style>
		<script>
		function showFilename(n,line) {
			hover = document.getElementById('info'+line)
			hover.innerHTML = document.getElementById('file'+n).innerHTML
		}
		function clearInfo(line) {
			hover = document.getElementById('info'+line)
			hover.innerHTML = ''
		}
		</script>
		</head>
		<body bgcolor=white>""")
		#date
		file.write("<p>This file was created automatically by user '<b>%s</b>' on <b>%s</b></p>\n" % (user, date))
		file.write("<p>Allowable error began at <b>%.2f</b> A and was capped at <b>%.2f</b> A.</p>\n" % (self.start_err, self.err-self.increment)) 
		#files
		file.write("""
		<table>
		<tr>
		<th colspan=2>PDB Files""")
		for i,pdb in enumerate(self.pdbs):
			file.write("""
			<tr>
			<td class='file_n'><pre>%3d  </pre>
			<td class='filename' id='file%d'>%s""" % (i+1, i, pdb.shortname))
		file.write('</table>\n')
		
		#header
		file.write("""
		<table>""")
		file.write("""
		<tr>
		<th class='res_num'>Res Num
		<th class='coor' colspan=3>Average Position
		<th class='rmsd'>RMSD
		<th class='file_n' colspan=""" + str(n_pdbs) + """>Files
		<th class='n_files'>#files""")
		#table
		for cluster in self.master:
			file.write("""
			<tr class='cluster' onclick="document.location='#%d'">
			<td class='res_num'><a name='top%d'></a>%d
			<td class='coor'>%.3f<td class='coor'>%.3f<td class='coor'>%.3f
			<td class='rmsd'>%s""" % tuple([cluster.res_num]*3+cluster.mean()+[cluster.rmsd_str()]))
			is_close = dict([[atom.pdb.filename, atom.distance_from(cluster.mean(), self.err)] for atom in cluster])
			n_matches = [0]*len(self.pdbs)
			for atom in cluster:
				n_matches[atom.pdb.number] += 1
			
			for i,pdb in enumerate(self.pdbs):
				file.write("""
				<td class='file_n' onMouseOver='showFilename(%d,%d)' onMouseOut='clearInfo(%d)'>""" % (i, cluster.res_num, cluster.res_num))
				if n_matches[i]:
					if(n_matches[i] > 1 or not is_close[pdb.filename]):
						file.write("*")
					file.write("%d" % (i+1))
					
			file.write("""
			<td class='n_files'>(%d)
			<td id='info%d' class='filename' width='400px'>""" % (len(cluster), cluster.res_num))
			
		file.write("""
		</table>
		<table>""")
		for cluster in self.master:
			file.write("""
			<a name='%d'><h1>%d</h1></a>""" % (cluster.res_num, cluster.res_num))
			file.write(("""
			<table>
			<tr class='cluster' onclick="document.location='#top%d'">
			<th colspan=3>Average
			""" + "<td class='coor'>%.3f"*3 + """
			<td class='rmsd'>%s
			<tr>
			<th class='filename' colspan=2>File
			<th> Line #
			<th class='coor' colspan=3> Position
			<th class='rmsd'> Distance""") % tuple([cluster.res_num] + cluster.mean() + [cluster.rmsd_str()]))
			for atom in cluster:
				file.write(("""
				<tr>
				<td class='filename'>%s:<td class='file_n'>%d<td>%d&nbsp;
				""" + "<td class='coor'>%.3f"*3 + """
				<td class='rmsd'>%.3f""") % ((atom.pdb.shortname, atom.pdb.number+1, atom.line_number) + atom.position() + (atom.distance_from(cluster.mean()),)))
			file.write("""
			</table>""")
		file.write("""
		</body>
		</html>""")			
	

	def renumber_clusters(self):
		for i,cluster in enumerate(self.master):
			cluster.renumber(i+1)
def run():
	argv = sys.argv[1:]
	def getArg(c, default):
		try:
			i = argv.index('-'+c)
			argv.pop(i)
			return argv.pop(i)
		except:
			return default
	root = getArg('r', 'Renumbered/')
	if(root[-1:] != '/'):
		root += '/'
	start_err = float(getArg('e', '1.4'))
	if(not os.path.exists(root)):
		print 'mkdir %s' % root
		shell('mkdir %s' % root)
	pdb_filenames = []
	if(argv):
		pdb_filenames = argv
	else:
		filenames = os.listdir(os.getcwd())
		for f in filenames:
			if(f[-4:] == '.pdb'):
				pdb_filenames.append(f)
	a = Analyzer(pdb_filenames, root, err=start_err)
	#a.run()
	input = ''
	
	while(True):
		input = re.split('\s*', raw_input(' >>> '))
		try:
			if(input[0]==''): del input[0]
			if(input[-1] == ''): del input[-1]
			cmd = input[0]
		except:
			continue
		if(cmd == 'quit'):
			a.write()
			break
		if(cmd == 'group'):
			try:
				max_err = float(input[1])
				if(max_err < a.err):
					continue
			except:
				max_err = None
			a.group_waters(max_err)
			continue
		if(cmd == 'view'):
			a.write()
			os.popen('konqueror %s/master.html' % root)
			continue
		print "%$#@!"
if(__name__=='__main__'):
	run()
	
	