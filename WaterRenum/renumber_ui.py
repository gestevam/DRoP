import os
import re
filenames = os.listdir(os.getcwd())
PDBs = []
for f in filenames:
	if(f[-4:]=='.pdb'):
		PDBs.append(f)
for i, pdb in enumerate(PDBs):
	print "%3d\t%s" % (i, pdb)

two_files = []
message = ''
while(len(two_files)!=2):
	print message
	print "Which two files should I use (original, new)?"
	input = raw_input()
	try:
		two_files = [PDBs[int(x)] for x in re.split(r'\s*,?\s*', input)]
		if(two_files[0] == two_files[1]): two_files = []
	except:
		two_files = []
	message = 'Please choose exactly *two* files.'

original_file, new_file = two_files
print
print "Original File:\t", original_file
print "New File:\t", new_file
print "Write to File:\t",
input = raw_input()
if(input == ''):
	write_file = 'renumbered.pdb'
else:
	write_file = input

from renumber import *

renumber_waters_in_file(original_file, new_file, write_file)
