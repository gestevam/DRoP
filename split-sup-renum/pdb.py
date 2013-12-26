water_names = ['HOH', 'H2O', 'OH2', 'WAT']
atom_names = ['ATOM', 'HETATM']
Infinity = 1e10

class Atom:
	"""
	type  atom_num   res_name      x       y       z       1.00  field
		atom_nam.res_num
			group
	s-----d----  s---s---sd---     f------ f------ f------ f---- f----
	012345678901234567890123456789012345678901234567890123456789012345678901234567890
	0         1         2         3         4         5         6         7         8
	"""
	strip = lambda s: s.strip()
	loc = {}
	loc['type'] = (0,6,'s')
	loc['atom name'] = (13,17,'s')
	loc['res name'] = (17,21,'s')
	loc['res num'] = (22,26,'d')
	loc['x'] = (31,38,'.3f')
	loc['y'] = (39,46,'.3f')
	loc['z'] = (46,54,'.3f')
	loc['chain'] = (21,22,'s')
	func = dict(f=float, d=int, s=strip)
	
	def __init__(self, line, line_number, pdb=None):
		self.line = line
		self.line_number = line_number
		self._position = None
		self.pdb = pdb
		self.cluster = None
		
	def __getitem__(self, key):
		(a,b,format) = Atom.loc[key]
		return Atom.func[format[-1]](self.line[a:b])
	def __setitem__(self, key, value):
		(a,b,format) = Atom.loc[key]
		if(format=='s'): left='-'
		else: left=''
		str_fmt = "%%%s%d%s" % (left, b-a, format)
		if(key in ['x','y','z']):
			self._position = None
		self.line = self.line[:a] + str_fmt % value + self.line[b:]
	#def distance_from(self, r):
	#	return ((self['x']-r[0])**2 + (self['y']-r[1])**2 + (self['z']-r[2])**2)**.5
	def distance_from(self,r,err=None):
		if(not err):
			return ((self['x']-r[0])**2 + (self['y']-r[1])**2 + (self['z']-r[2])**2)**.5
		p = self.position()
		if p == tuple(r):
			return True
		dx = (p[0]-r[0])
		if not (-err < dx < err): return False
		dy = (p[1]-r[1])
		if not (-err < dy < err): return False
		dz = (p[2]-r[2])
		if not (-err < dz < err): return False
		d2 = dx**2 + dy**2 + dz**2
		if(d2 < err**2):
			return d2**.5
		return False
	def position(self):
		if(self._position): return self._position
		self._position = (self['x'],self['y'],self['z'])
		return self._position
	def __str__(self):
		return self.line

class PDB(list):
	def __init__(self, filename=None, out_filename=None):
		list.__init__(self)
		self.filename = filename
		self.out_filename = out_filename
		if(filename):
			self.read()
	def read(self):
		file = open(self.filename, 'r')
		for i,line in enumerate(file.readlines()):
			self.append(Atom(line, i, pdb=self))
	def write(self):
		file = open(self.out_filename, 'w')
		for atom in self:
			file.write(str(atom))
	def __str__(self):
		return self.filename
