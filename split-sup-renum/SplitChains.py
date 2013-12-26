#!/usr/bin/python

#****************************************************************************
# SplitChains.py was created on July 2, 2008 by Daniel M. Roberts
# 
# This script splits non-water atoms into chains by their chain-label
# (usually 'A', 'B', etc.) and divides the waters among the chains
# by shortest distance.
# 
# Also keeps track of waters which are close
# to more than one chain. The default cutoff is 5.0 A, but you can
# specify your own in the commandline following '-e'.
#****************************************************************************

import sys, os, re
from pdb import *

class Chain(list):
	def __init__(self, name, atoms=[]):
		list.__init__(self)
		self.name = name
		for atom in atoms:
			self.append(atom)
	"""def shortest_distance_from(self, atom):
		w = atom.position()
		shortest = Infinity
		for chain_atom in self:
			d = chain_atom.distance_from(w, shortest)
			if d and d < shortest:
				shortest = d
		return shortest"""
	def __str__(self):
		s = 'Chain %s:\n' % self.name
		for atom in self:
			s += str(atom)
		return s
	def write(self, filename):
		pdb = PDB(out_filename=filename)
		for atom in self:
			pdb.append(atom)
		pdb.write()

class Splitter:
	cutoff = 5.
	def __init__(self, filename):
		self.pdb = PDB(filename)
		self.waters = []
		self.chains = {}
		self.water_chains = {}
		self.cutoff = 5.
		self.logfile = open('SplitChains_' + filename.split('/')[-1][:-4] +'.log', 'w')
		self.extract_data()
	def extract_data(self):
		self.waters = []
		self.chains = {}
		self.water_chains = {}
		for atom in self.pdb:
			if(atom['type'] not in atom_names):
				continue
			if(atom['res name'] in water_names):
				self.waters.append(atom)
			else:
				chain_name = atom['chain']
				if(chain_name):
					try:
						self.chains[chain_name].append(atom)
					except:
						self.chains[chain_name] = Chain(chain_name, [atom])
	def split(self, chain_names):
		chains_for_water = {}
		for water in self.waters:
			closest_chain, shortest_distance = ('', Infinity)
			chains_for_water[water] = []
			p = water.position()
			for chain_name in chain_names:
				for atom in self.chains[chain_name]:
					d = atom.distance_from(p, self.cutoff)
					if d:
						chains_for_water[water].append(chain_name)
						self.chains[chain_name].append(water)
						break
				
			"""if chains_for_water[water]:
				for chain_name in chains_for_water[water]:
					self.chains[chain_name].append(water)"""
			if not chains_for_water[water]:
				for chain_name in chain_names:
					for atom in self.chains[chain_name]:
						d = atom.distance_from(p, shortest_distance)
						if d and d < shortest_distance:
							closest_chain, shortest_distance = (chain_name, d)
				self.chains[closest_chain].append(water)
		if(not os.path.exists('split/')):
			os.popen('mkdir split')
		for chain_name in chain_names:
			self.chains[chain_name].write('split/' + self.pdb.filename.split('/')[-1][:-4] + '_chain-' + chain_name + '.pdb')
			#print Chain.__str__(chain)
		
		self.logfile.write('Waters far from all chains\n')
		for water, chain_names in chains_for_water.items():
			if(not chain_names):
				self.logfile.write(str(water))
		
		self.logfile.write('Waters close to two chains\n')
		for water, chain_names in chains_for_water.items():
			if len(chain_names) > 1:
				self.logfile.write('Chains %s\n%s' % (' and '.join(chain_names), water))
		
if(__name__=='__main__'):
	sys.argv.pop(0)
	try:
		i = sys.argv.index('-e')
		sys.argv.pop(i)
		cutoff = sys.argv.pop(i)
	except:
		cutoff = 5.0
	files = sys.argv
	if not files:
		files = filter(lambda x: x[-4:]=='.pdb', os.listdir(os.getcwd()))
	splitters = [Splitter(file) for file in files]

	"""print 'Chains Found:'
	ok_names = reduce(lambda x, y: x^y, [set(s.chains.keys()) for s in splitters])
	for chain_name in ok_names:
		print chain_name
	ok = False
	print 'Which chains do you want to include?'
	while not ok:
		chain_names = [chain_name.strip() for chain_name in re.split('\s*,?\s*', raw_input('$ '))]
		ok = True
		for chain_name in chain_names:
			if chain_name not in ok_names:
				print '$#@!'
				ok = False"""
	print 'Which chains do you want to include?'
	chain_names = [chain_name.strip() for chain_name in re.split('\s*,?\s*', raw_input('>>> '))]
	for s in splitters:
		s.cutoff = cutoff
		s.split(chain_names)