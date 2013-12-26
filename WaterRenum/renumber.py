from Scientific.IO.PDB import *

def renumber_waters_in_file(original_file, standard_file, write_file, err=1.4):
	original = Structure(original_file)
	new = Structure(standard_file)
	original_water_indicies = []
	new_water_indicies = []
	no_match = []
	max_serial_number = 0
	for i,residue in enumerate(original):
		if(residue.name == 'HOH'):
			original_water_indicies.append(i)
	for i,residue in enumerate(new):
		if(residue.name == 'HOH'):
			new_water_indicies.append(i)
	for i in original_water_indicies:
		for j in new_water_indicies:
			if((original[i][0].position - new[j][0].position).length() < 1.4):
				new_serial_number = new[j][0].properties['serial_number']
				original[i][0].properties['serial_number'] = new_serial_number
				if(new_serial_number > max_serial_number):
					max_serial_number = new_serial_number
			else:
				no_match.append(i)
	for i in no_match:
		max_serial_number += 1
		original[i][0].properties['serial_number'] = max_serial_number
	original.writeToFile(write_file)

if __name__ == '__main__':
	import sys
	try:
		original_file = sys.argv[1]
		standard_file = sys.argv[2]
	except:
		original_file = 'original.pdb'
		standard_file = 'standard.pdb'
	try:
		write_file = sys.argv[3]
	except:
		write_file = 'renumbered.pdb'
	renumber_waters_in_file(original_file, standard_file, write_file)
