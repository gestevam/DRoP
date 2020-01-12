from struct import *
def f(c):
 c = repr(c)
 if(c[1] == '\\'):
  if(c[2] == 'x'):
   c = c[3:-1]
 return "%4s" % c

dcd = open('1CTQ6000.DCD', 'r')
c = ' '
count = 0
chunk_size = 4
while c:
 c = dcd.read(chunk_size)
 count += chunk_size
 print repr(c),
 if(count > 20): break
 
print count
