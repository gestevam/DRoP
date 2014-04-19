#!/usr/bin/python

#*********************************************************************************
# pdb.py
# Version 1.0
# July 9, 2010 by Bradley M. Kearney
#
# Extension of pdb.py 
# Created July 1, 2008 by Daniel M. Roberts
#
#
# This program handles pdb files and formatting for DRoP.py. It also generates
# a variant of the cell linked-list for distance calculations.
#*********************************************************************************



water_names = ['HOH', 'H2O', 'OH2', 'WAT']
atom_names = ['ATOM', 'HETATM']
organic_names = []
exception_names = []
protein_names = ['GLY', 'ALA', 'VAL', 'LEU', 'ILE', 'PRO', 'ARG', 'ASN', 'ASP', 'CYS', 'GLU', 'GLN', 'HIS', 'LYS', 'MET', 'PHE', 'SER', 'THR', 'TRP', 'TYR', 'GNP']
Infinity = 1e10

import math
import sys
import time
import numpy
import datetime
import os
sys.setrecursionlimit(9999)

if(os.path.exists('config.txt')):
    file = open('config.txt', 'r')
    for line in file:       
        if not line[0] == "#":
            line = line.rstrip()
            for a in line.split(","):
                organic_names.append(a)
        else:
            line=line[1:]
            line = line.rstrip()
            for a in line.split(","):
                #print "IGI ARI! %s"%a
                exception_names.append(a)
    file.close()
else:
    print "*************!WARNING!*************"
    print "*        Missing config.txt       *"
    print "*     Organics NOT recognized     *"
    print "*************!WARNING!*************"
now = datetime.datetime.now()
 
     

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
    loc['line num'] = (7, 11, 'd')
    loc['type'] = (0, 6, 's')
    loc['atom name'] = (13, 17, 's')
    loc['res name'] = (17, 21, 's')
    loc['res num'] = (22, 26, 'd')
    loc['x'] = (30, 37, '.3f')
    loc['y'] = (38, 45, '.3f')
    loc['z'] = (46, 53, '.3f')
    loc['chain'] = (21, 22, 's')
    loc['B'] = (60, 65, '.3f')
    loc['atype'] = (77, 78, 's')
    func = dict(f=float, d=int, s=strip)


    def __init__(self, line, line_number, pdb, watercheck=0):
        self.line = line
        self.ores = self.line[22:26]
        self.line_number = line_number
        self._position = None
        self.pdb = pdb
        self.cluster = []
        self.close = 0
        self.clusterID = int(9999)
        self.space_group = pdb.space_group
        self.a = pdb.a
        self.b = pdb.b
        self.c = pdb.c
        self.isoutlier = 0
        self.out = []
        self.myname = pdb.filename
        self.alpha = pdb.alpha
        self.beta = pdb.beta
        self.gamma = pdb.gamma
        valid = water_names + protein_names + organic_names + exception_names
        if watercheck==1:
            if self['res name'] in water_names:
                self['res num']=self['line num']
        if self['type'] in atom_names:
            if self['res name'] not in valid:
                #print "UNKNOWN ATOM: " + self['res name']
                organic_names.append(self['res name'])
    def __getitem__(self, key):
        (a, b, format) = Atom.loc[key]
        return Atom.func[format[-1]](self.line[a:b])
    def __setitem__(self, key, value):
        (a, b, format) = Atom.loc[key]
        if type(value) == float:
            b = b + 1
            if(key.strip()=="B"):
                if (value<10):
                    whitespace="  "
                elif value<100:
                    whitespace=" "
                else:
                    whitespace=""
                value=str("%s%.2f"%(whitespace,value))
                format = 's'
            else:
                value=float(str("%.3f"%value))
        #newtype="%.3f"%value
        if(format == 's'): left = '-'
        else: left = ''
        str_fmt = "%%%s%d%s" % (left, b-a, format)
        if(key in ['x', 'y', 'z']):
            self._position = None
        self.line = self.line[:a] + str_fmt % value + self.line[b:]
    def coords(self):
        return [self['x'], self['y'], self['z']]

    def distance_from(self, r, err=None):
        if(not err):
            return ((self['x']-r[0]) ** 2 + (self['y']-r[1]) ** 2 + (self['z']-r[2]) ** 2) ** .5
        p = self.position()
        if p == tuple(r):
            return True
        dx = (p[0]-r[0])
        if not (-err < dx < err): return False
        dy = (p[1]-r[1])
        if not (-err < dy < err): return False
        dz = (p[2]-r[2])
        if not (-err < dz < err): return False
        d2 = dx ** 2 + dy ** 2 + dz ** 2
        if(d2 < err ** 2):
            return d2 ** .5
        return False
        
    def howclose(self):
        return self.close
        
    def optimum_update(self, optimum):
        self['x'] = float("%.3f" % optimum[0])
        self['y'] = float("%.3f" % optimum[1])
        self['z'] = float("%.3f" % optimum[2])
                
    def addclose(self):
        self.close = self.close + 1
                
    def setclose(self, count):
        self.close = count
                
    def position(self):
        if(self._position): return self._position
        self._position = (self['x'], self['y'], self['z'])
        return self._position
        
    def __str__(self):
        return self.line

class organic_molecule:
    def __init__(self,pass_atoms,mypdb):
        x=0
        y=0
        z=0
        self.cluster=None
        self.pdb=mypdb
        self.atoms=pass_atoms
        for atom in self.atoms:
            x+=atom.position()[0]
            y+=atom.position()[1]
            z+=atom.position()[2]
        x=x/len(self.atoms)
        y=y/len(self.atoms)
        z=z/len(self.atoms)
        self.center=[x,y,z]
        self.isoutlier=0
        self.ores = pass_atoms[0]['res num']                                  
        self.chain=pass_atoms[0]['chain']
    def position(self):
        return self.center
    def position2(self):
        return (self.center[0], self.center[1], self.center[2])
    def setresnum(self,toset):
        self.cluster=toset
        for i in self.atoms:
            i['res num']=toset
    def optimum_update(self,best):
        if best==None:
            return
        else:
            for i,j in zip(best.atoms,self.atoms):
                j.optimum_update(i.position())
            x=0
            y=0
            z=0
            for atom in self.atoms:
                x+=atom.position()[0]
                y+=atom.position()[1]
                z+=atom.position()[2]
            x=x/len(self.atoms)
            y=y/len(self.atoms)
            z=z/len(self.atoms)
            self.center=[x,y,z]
                #self.atoms[i].optimum_update(best[i])
    def distance_from(self, r, err=None):
        if(not err):
            return ((self.center[0]-r[0]) ** 2 + (self.center[1]-r[1]) ** 2 + (self.center[2]-r[2]) ** 2) ** .5
        p = self.position()
        if p == tuple(r):
            return True
        dx = (p[0]-r[0])
        if not (-err < dx < err): return False
        dy = (p[1]-r[1])
        if not (-err < dy < err): return False
        dz = (p[2]-r[2])
        if not (-err < dz < err): return False
        d2 = dx ** 2 + dy ** 2 + dz ** 2
        if(d2 < err ** 2):
            return d2 ** .5
        return False
        

class PDB(list):

    max_x = -1000.2
    max_y = -1000.3
    max_z = -1000.4
    min_x = 1000.2
    min_y = 1000.3
    min_z = 1000.4
    rx = 0
    ry = 0
    rz = 0
    lx = 0
    ly = 0
    lz = 0
    cutoff = 3.5
    cList = []
    wList = []
    flag = 0
    crys1 = 0
    
    def findneighbor(self, r, resnum, f2=0):
        #print self.cutoff
        #self.cutoff = 5
        cx = math.floor((-self.min_x + r[0]) / self.cutoff)
        cy = math.floor((-self.min_y + r[1]) / self.cutoff)
        cz = math.floor((-self.min_z + r[2]) / self.cutoff)
        cID = cx * self.ly * self.lz + cy * self.lz + cz
        flag=0
        if f2==1:
            flag=1
        else:
            flag=0
        neighbors = []
        trueneighbor = []
        if flag:
            print "%f %f %f"%(cx,cy,cz)
            print "%f %f %f"%(self.min_x, self.min_y, self.min_z)
            print "%f %f"%(cz-1,cz+2)
        for i in range(int(cx-1), int(cx + 2)):
            for j in range(int(cy-1), int(cy + 2)):
                for k in range(int(cz-1), int(cz + 2)):
                    if(i < 0 or j < 0 or k < 0):
                        if flag:
                            #print "%f %f %f"%(i,j,k)
                            print "negative range"
                        continue
                    else:
                        if(i > (self.lx-1) or j > (self.ly-1) or k > (self.lz-1)):
                            if flag:
                                print "positive range"
                            continue
                        else:
                            if flag:
                                print "just right"
                                print "%f %f %f"%(i,j,k)
                            tID = i * self.ly * self.lz + j * self.lz + k
                            if len(self.cList[int(tID)]) > 0:
                                if flag:
                                    print "adding a neighbor"
                                neighbors.append(self.cList[int(tID)])
        if len(neighbors) > 0:
            if(f2):
                print "I have more than one"
            for entry in neighbors:
                for neighbor in entry:
                    dx = (r[0]-float(neighbor['x']))
                    dy = (r[1]-float(neighbor['y']))
                    dz = (r[2]-float(neighbor['z']))
                    d2 = dx ** 2 + dy ** 2 + dz ** 2
                    if(d2 < self.cutoff ** 2):
                        if(neighbor['res num'] != resnum and neighbor['res name'] in protein_names):
                            if flag:
                                print "!!!!!!!!!!!!!PASSED!!!!!!!!!!!! %s %s %s %.3f"%(neighbor['res name'],neighbor['res num'],neighbor['atom name'],math.sqrt(d2))
                            trueneighbor.append(neighbor)
                    elif f2:
                         print "==============FAILED ============= %s %s %s %.3f"%(neighbor['res name'],neighbor['res num'],neighbor['atom name'],math.sqrt(d2))
        #self.cutoff = 3.5
        return trueneighbor

    def neighbor_distance(self, r, resnum):
        #print self.cutoff
        cx = math.floor((-self.min_x + r[0]) / self.cutoff)
        cy = math.floor((-self.min_y + r[1]) / self.cutoff)
        cz = math.floor((-self.min_z + r[2]) / self.cutoff)
        cID = cx * self.ly * self.lz + cy * self.lz + cz
        flag=0
        total=0
        count=0
        if (r[0]<-14 and r[0]>-15 and r[1]<55 and r[1]>50 and r[2]<-90 and r[2]>-100):
            #print r
            flag=0
        neighbors = []
        trueneighbor = []
        if flag:
            print "%f %f %f"%(cx,cy,cz)
            print "%f %f %f"%(self.min_x, self.min_y, self.min_z)
            print "%f %f"%(cz-1,cz+2)
        for i in range(int(cx-1), int(cx + 2)):
            for j in range(int(cy-1), int(cy + 2)):
                for k in range(int(cz-1), int(cz + 2)):
                    if(i < 0 or j < 0 or k < 0):
                        if flag:
                            print "%f %f %f"%(i,j,k)
                            print "negative range"
                        continue
                    else:
                        if(i > (self.lx-1) or j > (self.ly-1) or k > (self.lz-1)):
                            if flag:
                                print "positive range"
                            continue
                        else:
                            if flag:
                                print "just right"
                            tID = i * self.ly * self.lz + j * self.lz + k
                            if len(self.cList[int(tID)]) > 0:
                                if flag:
                                    print "adding a neighbor"
                                neighbors.append(self.cList[int(tID)])
        if len(neighbors) > 0:
            for entry in neighbors:
                for neighbor in entry:
                    dx = (r[0]-float(neighbor['x']))
                    dy = (r[1]-float(neighbor['y']))
                    dz = (r[2]-float(neighbor['z']))
                    d2 = dx ** 2 + dy ** 2 + dz ** 2
                    if(d2 < self.cutoff ** 2):
                        if(neighbor['res num'] != resnum and neighbor['res name'] in protein_names):
                            if flag:
                                print "%s %s %s %.3f"%(neighbor['res name'],neighbor['res num'],neighbor['atom name'],math.sqrt(d2))
                            count+=1
                            #print math.sqrt(d2)
                            total+=math.sqrt(d2)
        if count>0:
            #print "Returning: %f"%total
            return total
        else:
            return 0

    def setcutoff(self, newcutoff):
        self.cutoff = newcutoff
                
    def comparechain(self, r, chain):
        self.cutoff = 5
        cx = math.floor((-self.min_x + r[0]) / self.cutoff)
        cy = math.floor((-self.min_y + r[1]) / self.cutoff)
        cz = math.floor((-self.min_z + r[2]) / self.cutoff)
        cID = cx * self.ly * self.lz + cy * self.lz + cz
        neighbors = []
        count = 0
        for i in range(int(cx-1), int(cx + 2)):
            for j in range(int(cy-1), int(cy + 2)):
                for k in range(int(cz-1), int(cz + 2)):
                    if(i < 0 or j < 0 or k < 0):
                        break
                    else:
                        if(i > (self.lx-1) or j > (self.ly-1) or k > (self.lz-1)):
                            break
                        else:
                            tID = i * self.ly * self.lz + j * self.lz + k
                            if len(self.cList[int(tID)]) > 0:
                                neighbors.append(self.cList[int(tID)])
        if len(neighbors) > 0:
            for entry in neighbors:
                for neighbor in entry:
                    dx = (r[0]-float(neighbor['x']))
                    dy = (r[1]-float(neighbor['y']))
                    dz = (r[2]-float(neighbor['z']))
                    d2 = dx ** 2 + dy ** 2 + dz ** 2
                    if(d2 < self.cutoff ** 2 and neighbor['chain'] == chain):
                        count = count + 1
        return count

    def compare2(self, x):
        count = 0
        for r in x:
            cx = math.floor((-self.min_x + r[0]) / self.cutoff)
            cy = math.floor((-self.min_y + r[1]) / self.cutoff)
            cz = math.floor((-self.min_z + r[2]) / self.cutoff)
            cID = cx * self.ly * self.lz + cy * self.lz + cz
            neighbors = []
            for i in range(int(cx-1), int(cx + 2)):
                for j in range(int(cy-1), int(cy + 2)):
                    for k in range(int(cz-1), int(cz + 2)):
                        if(i < 0 or j < 0 or k < 0):
                            break
                        else:
                            if(i > (self.lx-1) or j > (self.ly-1) or k > (self.lz-1)):
                                break
                            else:
                                tID = i * self.ly * self.lz + j * self.lz + k
                                if len(self.cList[int(tID)]) > 0:
                                    neighbors.append(self.cList[int(tID)])
            if len(neighbors) > 0:
                for entry in neighbors:
                    for neighbor in entry:
                        dx = (r[0]-float(neighbor['x']))
                        dy = (r[1]-float(neighbor['y']))
                        dz = (r[2]-float(neighbor['z']))
                        d2 = dx ** 2 + dy ** 2 + dz ** 2
                        if(d2 < self.cutoff ** 2):
                            count = count + 1
        return count

    def compare(self, r):
        cx = math.floor((-self.min_x + r[0]) / self.cutoff)
        cy = math.floor((-self.min_y + r[1]) / self.cutoff)
        cz = math.floor((-self.min_z + r[2]) / self.cutoff)
        cID = cx * self.ly * self.lz + cy * self.lz + cz
        neighbors = []
        count = 0
        for i in range(int(cx-1), int(cx + 2)):
            for j in range(int(cy-1), int(cy + 2)):
                for k in range(int(cz-1), int(cz + 2)):
                    if(i < 0 or j < 0 or k < 0):
                        break
                    else:
                        if(i > (self.lx-1) or j > (self.ly-1) or k > (self.lz-1)):
                            break
                        else:
                            tID = i * self.ly * self.lz + j * self.lz + k
                            if len(self.cList[int(tID)]) > 0:
                                neighbors.append(self.cList[int(tID)])
        if len(neighbors) > 0:
            for entry in neighbors:
                for neighbor in entry:
                    dx = (r[0]-float(neighbor['x']))
                    dy = (r[1]-float(neighbor['y']))
                    dz = (r[2]-float(neighbor['z']))
                    d2 = dx ** 2 + dy ** 2 + dz ** 2
                    if(d2 < self.cutoff ** 2):
                        count = count + 1
        return count

    def create_cell_table(self):
        flag = 0
        atoms = []
        #define boundaries
        for atom in self:
            if(atom['type'] == "ATOM" or atom['type'] == "HETATM"):
                atoms.append(atom)
                if(float(atom['x']) > self.max_x):
                    self.max_x = atom['x']
                if(float(atom['y']) > self.max_y):
                    self.max_y = atom['y']
                if(float(atom['z']) > self.max_z):
                    self.max_z = atom['z']
                if(float(atom['x']) < self.min_x):
                    self.min_x = atom['x']
                if(float(atom['y']) < self.min_y):
                    self.min_y = atom['y']
                if(float(atom['z']) < self.min_z):
                    self.min_z = atom['z']
        #define length of system
        self.max_x = self.max_x + self.cutoff
        self.max_y = self.max_y + self.cutoff
        self.max_z = self.max_z + self.cutoff
        self.min_x = self.min_x-self.cutoff
        self.min_y = self.min_y-self.cutoff
        self.min_z = self.min_z-self.cutoff
        self.rx = self.max_x-self.min_x
        self.ry = self.max_y-self.min_y
        self.rz = self.max_z-self.min_z
        #define how many cells per direction
        self.lx = math.ceil(self.rx / self.cutoff)
        self.ly = math.ceil(self.ry / self.cutoff)
        self.lz = math.ceil(self.rz / self.cutoff)
        #create and populate cell list
        numcells = self.lx * self.ly * self.lz
        cList = []
        for i in xrange(int(numcells)):
            cList.append([])
        flag = 0
        for atom in atoms:
            if atom['res name'] in protein_names:
                cx = math.floor((-self.min_x + atom['x']) / self.cutoff)
                cy = math.floor((-self.min_y + atom['y']) / self.cutoff)
                cz = math.floor((-self.min_z + atom['z']) / self.cutoff)
                cID = cx * self.ly * self.lz + cy * self.lz + cz
                cList[int(cID)].append(atom)
        self.cList = cList
                
                
    def sortwaters(self):
        waters = []
        waterchain = 'A'
        endpos = self[0]
        kill = []
        chains = []
        sortchain = []
        finishedwaters = []
        startpos = -999
        i = 1
        j = -1
        for atom in self:
            j += 1
            if (atom['type'] in atom_names):
                if atom['res name'] not in water_names:
                    i = i + 1
                    endpos = atom
                else:
                    waters.append(atom)
                    kill.append(j)
                    waterchain = atom['chain']
        sortchain = sorted(waters, key=lambda x: x['res num'])
        for atom in sortchain:
            atom['line num'] = i
            i = i + 1
        i = 0
        sortchain2 = sorted(sortchain, key=lambda x: x['line num'])
        for atom in kill:
            self[atom] = sortchain2[i]
            i += 1
                    
    def sortorganics(self):
        waters = []
        waterchain = 'A'
        endpos = self[0]
        kill = []
        chains = []
        sortchain = []
        finishedwaters = []
        startpos = -999
        i = 1
        j = -1
        for atom in self:
            j += 1
            if (atom['type'] in atom_names):
                if atom['res name'] not in organic_names:
                    i = i + 1
                    endpos = atom
                else:
                    waters.append(atom)
                    kill.append(j)
                    waterchain = atom['chain']
        sortchain = sorted(waters, key=lambda x: x['line num'])
        for atom in sortchain:
            atom['line num'] = i
            i = i + 1
        i = 0
        sortchain2 = sorted(sortchain, key=lambda x: x['line num'])
        for atom in kill:
            self[atom] = sortchain2[i]
            i += 1

    def set_space(self, line):
        print self.filename
        self.space_group = line[54:65]
        print self.space_group
        self.space_group = self.space_group.rstrip()
        self.space_group = self.space_group.lstrip()
        self.myname = self.filename
        self.a = line[6:15]
        self.b = line[16:24]
        self.c = line[25:33]
        self.alpha = line[34:40]
        self.beta = line[41:47]
        self.gamma = line[48:54]

    def renumline(self):
        started = 0
        linenum = 1
        for atom in self:
            if not started:
                if atom['type'] in atom_names:
                    started = 1
                    atom['line num'] = linenum
                    linenum = linenum + 1
            else:
                if atom['type'] in atom_names:
                    atom['line num'] = linenum
                    linenum = linenum + 1
            
    def __init__(self, filename, out_filename=None, watercheck=0):
        list.__init__(self)
        self.space_group = None
        self.a = 0
        self.b = 0
        self.c = 0
        self.alpha = 0
        self.beta = 0
        self.gamma = 0
        self.filename = filename
        self.myname = filename
        self.watercheck=watercheck
        self.original_organics = []
        self.symmetry_organics = []
        self.original_centers = []
        self.symmetry_centers =[]
        if(out_filename == None):
            self.out_filename = filename
        else:
            self.out_filename = out_filename
        if(os.path.exists(filename)):
            self.read()

    def findsymms(self):
        self.zindex=[] #Contains resname and resnum for symmetry written organics
        self.sindex=[] #Contains resname and resnum for symmetry written waters

        self.zlist=[] #atom listing of symmetry written organics
        self.olist=[] #atom listing of original organics that have symmetry
        self.twlist={} #TotalWaterLIST
        self.tolist={}
        self.slist=[] #atom listing of symmetry written waters
        self.wlist=[] #atom listing of original waters that have symmetry
        curr_res=-1
        curr_name="Fred"
        dupcheck=[]
        test=[]
        test2={}
        curr_list=[]
        length=0
        flag=0
        for atom in self:
            if atom['type']=="ATOM" or atom['type']=="HETATM": #I'm looking at an atom
                if atom['chain']=='Z': #I'm in the right chain
                    if curr_res !=atom['res num'] or curr_name!=atom['res name']: #This atom isn't the current one I'm working on...
                        if curr_name=="Fred":
                            curr_res=atom['res num']
                            curr_name=atom['res name']
                            test.append(atom)
                        else:
                            count=0
                            test2={}
                            for i in test:
                                if i['atom name'] not in dupcheck:
                                    if count not in test2:
                                        test2[count]=[]
                                    count=0
                                    test2[count].append(i)
                                    dupcheck=[]
                                    dupcheck.append(i['atom name'])
                                else:
                                    count+=1
                                    if count not in test2:
                                        test2[count]=[]
                                    test2[count].append(i)
                            for i in test2:
                                if "%s%d"%(test2[i][0]['res name'],test2[i][0]['res num']) not in self.tolist:
                                    self.tolist["%s%d"%(test2[i][0]['res name'],test2[i][0]['res num'])]=[]
                                self.tolist["%s%d"%(test2[i][0]['res name'],test2[i][0]['res num'])].append(organic_molecule(test2[i],test2[i][0].pdb))
                            test=[]
                            test.append(atom)
                            curr_res=atom['res num']
                            curr_name=atom['res name']
                    else:
                        test.append(atom)                            
                   
                if atom['chain']=='S':
                    self.sindex.append("%s%d"%(atom['res name'],atom['res num']))
                    self.slist.append(atom)
                    if "%s%d"%(atom['res name'],atom['res num']) not in self.twlist:
                        self.twlist["%s%d"%(atom['res name'],atom['res num'])]=[]
                    self.twlist["%s%d"%(atom['res name'],atom['res num'])].append(atom)
        count=0
        dupcheck=[]
        test2={}
        for i in test:
            if i['atom name'] not in dupcheck:
                if count not in test2:
                    test2[count]=[]
                count=0
                test2[count].append(i)
                dupcheck=[]
                dupcheck.append(i['atom name'])
            else:
                count+=1
                if count not in test2:
                    test2[count]=[]
                test2[count].append(i)
        for i in test2:
            if "%s%d"%(test2[i][0]['res name'],test2[i][0]['res num']) not in self.tolist:
                self.tolist["%s%d"%(test2[i][0]['res name'],test2[i][0]['res num'])]=[]
            self.tolist["%s%d"%(test2[i][0]['res name'],test2[i][0]['res num'])].append(organic_molecule(test2[i],test2[i][0].pdb))
        test=[]
        curr_res=-1
        curr_name="Fred"
        for atom in self:
            if atom['type']=="ATOM" or atom['type']=="HETATM":
                if atom['chain']=='O':
                    if curr_res !=atom['res num'] or curr_name!=atom['res name']: #This atom isn't the current one I'm working on...
                        if curr_name=="Fred":
                            curr_res=atom['res num']
                            curr_name=atom['res name']
                            test.append(atom)
                        else:
                            count=0
                            test2={}
                            for i in test:
                                if i['atom name'] not in dupcheck:
                                    if count not in test2:
                                        test2[count]=[]
                                    count=0
                                    test2[count].append(i)
                                    dupcheck=[]
                                    dupcheck.append(i['atom name'])
                                else:
                                    count+=1
                                    if count not in test2:
                                        test2[count]=[]
                                    test2[count].append(i)
                            for i in test2:
                                if "%s%d"%(test2[i][0]['res name'],test2[i][0]['res num']) not in self.tolist:
                                    self.tolist["%s%d"%(test2[i][0]['res name'],test2[i][0]['res num'])]=[]
                                molecule=organic_molecule(test2[i],test2[i][0].pdb)
                                self.tolist["%s%d"%(test2[i][0]['res name'],test2[i][0]['res num'])].append(molecule)
                                self.olist.append(molecule)
                            test=[]
                            test.append(atom)
                            curr_res=atom['res num']
                            curr_name=atom['res name']
                    else:
                        test.append(atom)
                if atom['chain']=='W':
                    if "%s%d"%(atom['res name'],atom['res num']) in self.sindex:
                        self.wlist.append(atom)
                        self.twlist["%s%d"%(atom['res name'],atom['res num'])].append(atom)
                count=0
        dupcheck=[]
        test2={}
        for i in test:
            if i['atom name'] not in dupcheck:
                if count not in test2:
                    test2[count]=[]
                count=0
                test2[count].append(i)
                dupcheck=[]
                dupcheck.append(i['atom name'])
            else:
                count+=1
                if count not in test2:
                    test2[count]=[]
                test2[count].append(i)
        for i in test2:
            if "%s%d"%(test2[i][0]['res name'],test2[i][0]['res num']) not in self.tolist:
                self.tolist["%s%d"%(test2[i][0]['res name'],test2[i][0]['res num'])]=[]
            molecule=organic_molecule(test2[i],test2[i][0].pdb)
            self.tolist["%s%d"%(test2[i][0]['res name'],test2[i][0]['res num'])].append(molecule)
            self.olist.append(molecule)

    def read(self):
        file = open(self.filename, 'r')
        for i, line in enumerate(file.readlines()):
            if line[0:6] == "CRYST1":
                self.set_space(line)
                self.crys1 = 1
            if line[0:3] == "END":
                continue
            line = line.rstrip()
            self.append(Atom(line, i, pdb=self, watercheck=self.watercheck))
            
    def write(self,stamp,flag=0):
        self.sortwaters()
        self.sortorganics()
        self.renumline()
        needend = 1
        started = 0
        self.out_filename = self.out_filename.replace('Renumbered/', '../../../results/%d/'%int(stamp))
        if flag==1:
            self.out_filename=self.out_filename[:-4] + "PRESUPER" + self.out_filename[-4:]
        if flag==2:
            self.out_filename.replace("PRESUPER","FINAL")
        file = open(str(self.out_filename), 'w')
        for atom in self:
            if(str(atom)[0:6] == "CONECT"):
                continue
            if(str(atom)[0:6] == "CRYST1"):
                if flag==1:
                    file.write("REMARK  \n")
                    file.write("REMARK     PROCESSED BY PREDROP\n")
                    file.write("REMARK     THIS FILE IS NOT TO BE DEPOSITED TO THE PDB\n")
                if flag==2:
                    file.write("REMARK    \n")
                    file.write("REMARK     SOLVENT POSITIONS OPTIMIZED AND RENUMBERED\n")
                    file.write("REMARK       PROGRAM     : DRoP (DRoP.ver: 1.0.0)\n")
                    file.write("REMARK       AUTHORS     : Kearney, Roberts, Dechene, Swartz, Mattos\n")
            if(str(atom)[0:3] == "END"):
                needend = 0
            if flag==2:
                if atom['type'] in atom_names:          
                    if(atom['chain']!='S' and atom['chain']!='Z'):
                        file.write(str(atom))
                        file.write('\n')
                else:
                        file.write(str(atom))
                        file.write('\n')
            else:
                file.write(str(atom))
                file.write('\n')
        if(needend):
            file.write("END")
    def writenew(self):
        if(not os.path.exists('Renumbered/' + stamp + '/')):
            os.makedirs('Renumbered/' + stamp)
        self.out_filename = self.out_filename.replace('Renumbered/', 'Renumbered/' + stamp + '/')
        file = open(str(self.out_filename), 'w')
        for atom in self:
                file.write(str(atom))
    def __str__(self):
        return self.filename

