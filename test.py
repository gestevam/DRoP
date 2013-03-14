import urllib
import sys

def run():
	argv = sys.argv[1:]
	i=0
	try: 
		i=int(argv.pop())
	except:
		print "oops"	
	variable=1
	print "the variable you passed was: %d"%i
	urllib.urlopen("http://129.10.89.145/running.php?session=%d"%variable)

	#file=open('results/writing.txt','w')
	#file.write('I just ran this program!')

if(__name__ == '__main__'):
	run()
