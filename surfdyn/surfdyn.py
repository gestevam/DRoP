from struct import *
import os
import re

class Reader:
	def __init__(self, filename):
		self.datafile = open(filename, 'r')
		self.import_header()

	def import_header(self):
		pass

	def skip(self, bytes = 4):
		self.datafile.read(bytes)

	def read_raw(self, bytes = 4):
		return self.datafile.read(bytes)


class FortranFormattedReader(Reader):
	def readline(self):
		return self.datafile.readline()


class FortranUnformattedReader(Reader):
	def read(self, *formats):
		self.skip()
		values = []
		for format in formats:
			if(type(format)==type(1)):
				values.append( self.read_raw(format) )
			else:
				values.append(  unpack(format, self.read_raw(calcsize(format)))  )
			if(len(values[-1])==1):
				values[-1] = values[-1][0]
		self.skip()
		if(len(values)==1):
			return values[0]
		return tuple(values)

	def read_string(self, size=80):
		self.skip()
		(n,) = unpack('l', self.read_raw(4))
		value = self.read_raw(size*n)
		self.skip()
		return value

class DCD(FortranUnformattedReader):
	"""field
	res_name
	atom_name
	segment_name
	segment
	title
	title_count
	total_atoms
	atom_n
	res_n
	res_n"""

	def import_header(self):
		(self.file_type, self.icntrl) = self.read(4, 'l'*9)
		self.title = self.read_string()
  
	def frames(self):
		dcd_total = self.read('l')
		n_fixed_atoms = self.icntrl[8]
		n_atoms = dcd_total - n_fixed_atoms
		if(n_fixed_atoms != 0):
			self.bs = self.read(80)
			yield self.bs
		frame_n = 0
		x = y = z = []
		while 1:
			frame_n += 1
			if(frame_n == 1):
				x = self.read('f'*dcd_total)
				y = self.read('f'*dcd_total)
				z = self.read('f'*dcd_total)
			else:
				x = x[:n_fixed_atoms] + self.read('f'*n_atoms)
				y = y[:n_fixed_atoms] + self.read('f'*n_atoms)
				z = z[:n_fixed_atoms] + self.read('f'*n_atoms)
			yield (frame_n-1, x,y,z)


class CRD(FortranFormattedReader):

	def import_header(self):
		self.comment = ''
		while 1:
			l = self.readline()
			if l[0]=='*':
				self.comment += l
			else:
				self.n_atoms = int(l)
				break

	def import_data(self):
		self.data = []
		self.keys = ['atom num', 'res num', 'res name', 'atom name', 'x', 'y', 'z', 'seg name', 'res num 2', 'field']
		types = (int, int, str, str, float, float, float, str, int, float)
		for line in self.datafile.readlines():
			entries = re.split(r'\s*', line)[:-1]
			if entries[0] == '':
				del entries[0]
			entries = [types[i](entries[i]) for i in range(10)]
			self.data.append(entries)
	def getData(self, frame_index, key):
		return self.data[frame_index][self.keys.index(key)]
	def getEntry(self, frame_index):
		return self.data[frame_index]


class SurfaceCalculator:
	def __init__(self, dcd=None, crd=None):
		base = '.'.join(dcd.split('.')[:-1])
		#files					#Fortran numbering
		self.log = ''					#7
		self.dcd = DCD(dcd)				#2
		self.crd = CRD(crd)				#4
		self.surf = open(base+'surf.dcd', 'w')	#8
		self.fluc = open(base+'fluc', 'w')		#9
		self.crd.import_data()
	
	def save_fluc(self):
		self.fluc.write("""
		Solvent Accessible Surface  Molecular Surface      
	DCD Frame Phylic   Phobic   Total     Phylic   Phobic   Total
""")
	class Frame:
		def __init__(self, meta):
			self.setMeta(meta)
		def setIXYZ(self, IXYZ):
			self.i, self.x_s, self.y_s, self.z_s = IXYZ
		def setMeta(self, meta):
			arrays = ([],[],[],[],[],[],[],[],[],[])
			(self.atom_nums, self.res_nums, self.res_names, self.atom_names,
				self.x_s, self.y_s, self.z_s, self.seg_names, self.res_nums_2, self.fields) = arrays
			for entry in meta:
				for i,array in enumerate(arrays):
					array.append(entry[i])
						
	def frames(self):
		dcd_frames = self.dcd.frames()
		
		frame = self.Frame(self.crd.data)
		for dcd_frame in dcd_frames:
			frame.setIXYZ(dcd_frame)
			yield frame
			
	def calculate(self):
		"""Calculates in steps"""
		for frame in self.frames():
			self.make_temp_pdb(frame)
			self.surface(frame)
			break
	
	def make_temp_pdb(self, frame):
		n_atoms = len(frame.x_s)
		pdb = open('temp.pdb', 'w')
		print n_atoms
		print len(frame.atom_names)
		try:
			for i in range(n_atoms):
				pdb.write("%-6s%5d  %-4s%-4s%-1s%4d     %7.3f %7.3f %7.3f %5.2f %5.2f\n" % ('ATOM', i+1, frame.atom_names[i], frame.res_names[i], 'A', frame.res_nums[i], frame.x_s[i], frame.y_s[i], frame.z_s[i], 1.00, frame.fields[i]))
		except:
			pass
	def surface(self, frame):
		probe = 1.40
		command = './ms.x -r %f -p temp.pdb -a temp1.ms > temp1.out' % probe
		os.popen(command)
if __name__ == '__main__':
	"""
	dcd = DCD('1CTQ6000.DCD')
	for frame in dcd.frames():
	l = len(frame[0])
	for i in range(l):
	print "/",
	for num in ["%.0f" % w[i] for w in frame]:
	print num,
	
	crd = CRD('1CTQAW62.CRD')
	print crd.comment
	print crd.n_atoms
	crd.import_data()
	print crd.data
	"""
	calculator = SurfaceCalculator(dcd='1CTQ6000.DCD', crd='1CTQAW62.CRD')
	calculator.calculate()
	calculator.save_fluc()
