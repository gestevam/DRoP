#/usr/bin/python
#*********************************************************************************
# preDRoP.py
# Feb. 26, 2011
# Bradley Kearney
# Processes pdb files for DRoP analysis.
#*********************************************************************************

from math import *
import sys
import time
import webbrowser
import datetime
import os
import copy
from pdb import *
from copy import deepcopy
import random
import re
import symgen
import urllib
import zipfile 
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
import numpy as np


def progressbar(it, count, prefix = "", size = 60):
    def _show(_i):
        x = int(size*_i/count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), _i, count))
        sys.stdout.flush()
    _show(it)
    if it==count:
        sys.stdout.write("\n")
        sys.stdout.flush()

def shell(cmd):
    return -1

class Cluster(list):
    def __init__(self, atom=None):
        list.__init__(self)
        self.sum = [0.] * 3
        """     self.a_sum = 0
        self.b_sum = 0
        self.c_sum = 0
        self.a = 0
        self.b = 0
        self.c = 0"""
        self.res_num = None
        self.percent = 0.00
        if not atom==None:
            #print "you passed me a none atom."
            self.append(atom)
    def append(self, atom):
        list.append(self, atom)
        """self.a_sum += float(atom.a)
        self.b_sum += float(atom.b)
        self.c_sum += float(atom.c)
        self.a = self.a_sum / len(self)
        self.b = self.b_sum / len(self)
        self.c = self.c_sum / len(self)"""
        atom.cluster = self
        self.sum = [self.sum[i] + atom.position()[i] for i in range(3)]
        self.reset_calculated_values()
        atom.clusterID = self.res_num
    def remove(self, atom):
        self.sum = [self.sum[i]-atom.position()[i] for i in range(3)]
        list.remove(self, atom)
        atom.cluster = None
        #ok busting out the big guns
        self.sum = [0.] * 3
        for j in self:
            self.sum = [self.sum[i] + j.position()[i] for i in range(3)]
        self.reset_calculated_values()
    def reset_calculated_values(self):
        self._mean = self._sd = self._sig = None
    def distance_from(self, comp):
        dx = (self.mean()[0]-comp[0])
        dy = (self.mean()[1]-comp[1])
        dz = (self.mean()[2]-comp[2])
        d2 = dx ** 2 + dy ** 2 + dz ** 2
        return d2 ** .5
    def contacts(self):
        total = 0
        for atom in self:
            total += atom.howclose()
        return total / (len(self))
    def atom_for_pdb(self, i):
        for atom in self:
            if atom.pdb.number == i:
                return atom
    def renumber(self, res_num):
        self.res_num = res_num
        for atom in self:
            atom['res num'] = res_num
    def mean(self):
        if(self._mean): return self._mean
        l = len(self)
        self._mean = [coor / l for coor in self.sum]
        return self._mean
    def avg_b(self):
        totb = 0
        for atom in self:
            totb = totb + atom['B']
        return totb / (len(self))
    def sig_b(self):
        if(self._sig): return self._sig
        mean = self.avg_b()
        sd = sum([sum([(mean-atom['B']) ** 2]) for atom in self])
        try:
            sd /= len(self)-1
        except:
            return 0
        self._sig = sd ** .5
        return self._sig
    def std_dev(self):
        if(self._sd): return self._sd
        mean = self.mean()
        sd = sum([sum([(mean[i]-atom.position()[i]) ** 2 for i in range(3)]) for atom in self])
        try:
            sd /= len(self)-1
        except:
            return Infinity
        self._sd = sd ** .5
        return self._sd
    def rmsd_str(self, na='N/A'):
        v = self.std_dev()
        if(v == Infinity): return na
        else: return "%.3f" % v
    def estimate_fit(self, atom, err):
        if atom.cluster == self:
            return atom.distance_from(self.mean(), err * (1. + 1. / len(self)))
        else:
            return atom.distance_from(self.mean(), err)
                
                
    def cmp(self, rhs):
        self_len, rhs_len = len(self), len(rhs)
        if(self_len == rhs_len):
            if(self_len == 1):
                return cmp(self[0].pdb.number, rhs[0].pdb.number)
            return cmp(self.std_dev(), rhs.std_dev())
        else: return -cmp(self_len, rhs_len)

class Ocluster(list):
    def __init__(self, atom):
        list.__init__(self)
        self.sum = [0.] * 3
        self.res_num = None
        self.append(atom)
    def append(self, atom):
        list.append(self, atom)
        atom.cluster = self
        self.sum = [self.sum[i] + atom.position()[i] for i in range(3)]
        self.reset_calculated_values()
    def remove(self, atom):
        list.remove(self, atom)
        atom.cluster = None
        self.sum = [0.] * 3
        for j in self:
            self.sum = [self.sum[i] + j.position()[i] for i in range(3)]
        self.reset_calculated_values()
    def reset_calculated_values(self):
        self._mean = self._sd = None
    def distance_from(self, comp):
        dx = (self.mean()[0]-comp[0])
        dy = (self.mean()[1]-comp[1])
        dz = (self.mean()[2]-comp[2])
        d2 = dx ** 2 + dy ** 2 + dz ** 2
        return d2 ** .5
    def contacts(self):
        total = 0
        for atom in self:
            total += atom.howclose()
            #print total
        return total / (len(self))
    def atom_for_pdb(self, i):
        for atom in self:
            if atom.pdb.number == i:
                return atom
    def renumber(self, res_num):
        self.res_num = res_num
        for atom in self:
            atom.setresnum(res_num)
    def mean(self):
        if(self._mean): return self._mean
        l = len(self)
        self._mean = [coor / l for coor in self.sum]
        return self._mean
    def std_dev(self):
        if(self._sd): return self._sd
        mean = self.mean()
        sd = sum([sum([(mean[i]-atom.position()[i]) ** 2 for i in range(3)]) for atom in self])
        try:
            sd /= len(self)-1
        except:
            return Infinity
        self._sd = sd ** .5
        return self._sd
    def rmsd_str(self, na='N/A'):
        v = self.std_dev()
        if(v == Infinity): return na
        else: return "%.3f" % v
    def estimate_fit(self, atom, err):
        if atom.cluster == self:
            return atom.distance_from(self.mean(), err * (1. + 1. / len(self)))
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
    stamp= now.strftime("%Y%m%d_%H%M%S") + '/'

    def sortthis(self):
        self.waters = sorted(self.waters, key=lambda x: x['res num'])
    def sortthat(self):
        self.organics = sorted(self.organics, key=lambda x: x['res num'])
                
    class Ocluster_List(list):
        def move(self, atom, cluster):
            if(id(atom.cluster) == id(cluster) or not cluster):
                raise Exception
            if(atom.cluster):
                old_cluster = atom.cluster
                old_cluster.remove(atom)
                if(len(old_cluster) == 0):
                    if old_cluster in self:
                        self.remove(old_cluster)
            cluster.append(atom)
        def move2(self, atom, rematom, cluster):
            if(id(atom.cluster) == id(cluster) or not cluster):
                raise Exception
            if(atom.cluster):
                old_cluster = atom.cluster
                old_cluster.remove(rematom)
                if(len(old_cluster) == 0):
                    if old_cluster in self:
                        self.remove(old_cluster)
            cluster.append(atom)
        def isolate(self, atom):
            if(not atom.cluster):
                raise Exception
            old_cluster = atom.cluster
            old_cluster.remove(atom)
            if(not old_cluster):
                self.remove(old_cluster)
            self.append(Ocluster(atom))
                
    class Cluster_List(list):
        def move(self, atom, cluster):
            if(id(atom.cluster) == id(cluster) or not cluster):
                raise Exception
            if(atom.cluster):
                old_cluster = atom.cluster
                old_cluster.remove(atom)
                if(len(old_cluster) == 0):
                    if old_cluster in self:
                        self.remove(old_cluster)
            cluster.append(atom)
        def move2(self, atom, rematom, cluster):
            if(id(atom.cluster) == id(cluster) or not cluster):
                raise Exception
            if(atom.cluster):
                old_cluster = atom.cluster
                old_cluster.remove(rematom)
                if(len(old_cluster) == 0):
                    if old_cluster in self:
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
                        

    def __init__(self, pdb_filenames, root, id, err=1):
        self.pdbs = []
        self.id=id
        totalnum = 0
        for filename in pdb_filenames:
            self.pdbs.append(PDB(filename, root + filename.split('/')[-1]))
        self.pdbs.sort(key=str)
        for i, pdb in enumerate(self.pdbs):
            pdb.number = i
            pdb.shortname = pdb.filename.split('/')[-1]
            totalnum = i
        self.waters = []
        self.aa = []
        self.organics = []
        self.wList = []
        self.oList = []
        self.max_x = -1000.2
        self.max_y = -1000.3
        self.max_z = -1000.4
        self.min_x = 1000.2
        self.min_y = 1000.3
        self.min_z = 1000.4
        self.rx = 0
        self.ry = 0
        self.rz = 0
        self.lx = 0
        self.ly = 0
        self.lz = 0
        self.cutoff = 5
        shortest_distance = ('', Infinity)
        for pdb in self.pdbs:
            pdb.create_cell_table()
                                    
        #Create Water Table
        flag = 0
        waters = []
        #define boundaries
        for atom in self.waters:
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
        for atom in self.waters:
            cx = math.floor((-self.min_x + atom['x']) / self.cutoff)
            cy = math.floor((-self.min_y + atom['y']) / self.cutoff)
            cz = math.floor((-self.min_z + atom['z']) / self.cutoff)
            cID = cx * self.ly * self.lz + cy * self.lz + cz
            cList[int(cID)].append(atom)
        self.wList = cList
        #End Water Table
                
        count = 0
        numwater = float(len(self.waters))
        numorg = len(self.organics)
        debug = 0
        if(debug == 0):
            print "Calculating nearby contacts for waters."
            for w in self.waters:
                count = count + 1
                for pdb in self.pdbs:
                    if (pdb == w.pdb):
                        w.setclose(pdb.compare(w.position()))
            print "Calculating nearby contacts for organics/ligands."
            for o in self.organics:
                for pdb in self.pdbs:
                    if (pdb == o.pdb):
                        o.setclose(pdb.compare(o.position()))
        self.root = root + self.stamp
        if(not os.path.exists(self.root)):
            os.makedirs(self.root)
        self.master = Analyzer.Cluster_List()
        self.master_org = Analyzer.Ocluster_List()
        self.master_path = '../../../results/%d/master.html'%self.id
        self.orgmaster_path = '../../../results/%d/org.html'%self.id
        self.err = self.start_err = 1.0
        self.orgerr = 1.0
        self.centers = []

    def recreatewater(self):
        flag = 0
        waters = []
        #define boundaries
        for atom in self.waters:
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
        for atom in self.waters:
            cx = math.floor((-self.min_x + atom['x']) / self.cutoff)
            cy = math.floor((-self.min_y + atom['y']) / self.cutoff)
            cz = math.floor((-self.min_z + atom['z']) / self.cutoff)
            cID = cx * self.ly * self.lz + cy * self.lz + cz
            cList[int(cID)].append(atom)
        self.wList = cList

    def recreateorganic(self):
        flag = 0
        numcells = self.lx * self.ly * self.lz
        cList = []
        for i in xrange(int(numcells)):
            cList.append([])
        flag = 0
        for atom in self.organiclist:
            cx = math.floor((-self.min_x + atom.position()[0]) / self.cutoff)
            cy = math.floor((-self.min_y + atom.position()[1]) / self.cutoff)
            cz = math.floor((-self.min_z + atom.position()[2]) / self.cutoff)
            cID = cx * self.ly * self.lz + cy * self.lz + cz
            cList[int(cID)].append(atom)
        self.oList = cList

    def createlist(self):
        symms=['S','Z']
        self.waters=[]
        self.organiclist=[]
        for pdb in self.pdbs:
            for atom in pdb:
                if atom['chain'] not in symms:
                    if(atom['type'] == "ATOM" or atom['type'] == "HETATM"):
                        if(atom['res name'] in water_names):
                            self.waters.append(atom)
                        if(atom['res name'] in protein_names):
                            self.aa.append(atom)
            for i in pdb.olist:
                self.organiclist.append(i)
        self.recreatewater()
        self.recreateorganic()

    def createlist2(self):
        self.waters=[]
        self.organiclist=[]
        count=0
        for pdb in self.pdbs:
            for i in pdb.olist:
                self.organiclist.append(i)
        """for i in self.master_org:
            for j in i:
                count+=1
                self.organiclist.append(j)
        """
        for i in self.master:
            for j in i:
                count+=1
                self.waters.append(j)
        self.recreatewater()
        self.recreateorganic()


    def proximal_organics(self, r, err):
        cx = math.floor((-self.min_x + r[0]) / self.cutoff)
        cy = math.floor((-self.min_y + r[1]) / self.cutoff)
        cz = math.floor((-self.min_z + r[2]) / self.cutoff)

        cID = cx * self.ly * self.lz + cy * self.lz + cz
        neighbors = []
        goodneighbors = []
        checkpdb=[]
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
                            if tID>len(self.oList):
                                continue
                            if len(self.oList[int(tID)]) > 0:
                                neighbors.append(self.oList[int(tID)])
        if len(neighbors) > 0:
            for entry in neighbors:
                for neighbor in entry:
                    dx = (r[0]-float(neighbor.position()[0]))
                    dy = (r[1]-float(neighbor.position()[1]))
                    dz = (r[2]-float(neighbor.position()[2]))
                    d2 = dx ** 2 + dy ** 2 + dz ** 2
                    if(d2 < err ** 2):
                        goodneighbors.append(neighbor)
        return goodneighbors

    def proximal_waters(self, r, err):
        cx = math.floor((-self.min_x + r[0]) / self.cutoff)
        cy = math.floor((-self.min_y + r[1]) / self.cutoff)
        cz = math.floor((-self.min_z + r[2]) / self.cutoff)

        cID = cx * self.ly * self.lz + cy * self.lz + cz
        neighbors = []
        goodneighbors = []
        checkpdb=[]
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
                            if len(self.wList[int(tID)]) > 0:
                                neighbors.append(self.wList[int(tID)])
        if len(neighbors) > 0:
            for entry in neighbors:
                for neighbor in entry:
                    dx = (r[0]-float(neighbor['x']))
                    dy = (r[1]-float(neighbor['y']))
                    dz = (r[2]-float(neighbor['z']))
                    d2 = dx ** 2 + dy ** 2 + dz ** 2
                    if(d2 < err ** 2 and not neighbor.pdb in checkpdb):
                        goodneighbors.append(neighbor)
                        checkpdb.append(neighbor.pdb)
        return goodneighbors
    
    def renumber_clusters(self):
        for i, cluster in enumerate(self.master):
            cluster.renumber(i + 1)
    def renumber_orgclusters(self):
        for i, cluster in enumerate(self.master_org):
            cluster.renumber(i + 1)

    def newgroup22(self, max_err):
        self.master=[]
        done = 0
        self.magi +=1
        pool = []
        print len(self.waters)
        pool.extend(self.waters)
        maxsize=len(self.waters)
        random.shuffle(pool)
        candidatelist = []
        candidate = []
        ties = []
        for i in pool:
            candidatewater = i
            candidatelist.append(self.proximal_waters(candidatewater.position(), max_err))
            largest = 0   
        while not done:
            largest=0
            #progressbar(maxsize-len(pool),maxsize, "Processing waters: ")
            for i in candidatelist:
                if len(i) == largest:
                    ties.append(i)
                if len(i) > largest:
                    largest = len(i)
                    ties = []
                    ties.append(i)
            bestcluster = []
            bestrmsd = 999
            for i in ties:
                tempcluster = []
                tempcluster.extend(i)
                temp = Cluster()
                #i.pop(0)
                for j in i:
                    temp.append(j)
                if(bestrmsd > temp.std_dev()):
                    bestcluster = temp
                    bestrmsd = temp.std_dev()
            candidate = bestcluster
            #print largest
            if(len(candidate) == 0):
                candidate.append(pool[0])
            for i in candidatelist:
                if candidate[0] in i:
                    i.remove(candidate[0])
            newcluster = Cluster(candidate[0])
            pool.remove(candidate[0])
            for j in self.wList:
                if candidate[0] in j:
                    j.remove(candidate[0])
            candidate.pop(0)
            for i in candidate:
                pool.remove(i)
                newcluster.append(i)
                for j in candidatelist:
                    if i in j:
                        j.remove(i)
                for j in self.wList:
                    if i in j:
                        j.remove(i)
            #print "Appending cluster: %s"%newcluster
            self.master.append(newcluster)
            if len(pool) < 1:
                done = 1
            #print "Round complete. Number of waters ungrouped = %d"%len(pool)
        progressbar(maxsize,maxsize, "Processing waters: ")
        self.master.sort(Cluster.cmp)
        self.renumber_clusters()
        self.sortthis()
        maxwater = len(self.master[0])
        minwater = len(self.master[-1])
        demo = []
        self.master_len=maxwater
        if self.magi==0:
            self.water_table=[]
            self.water_table_post=[]
        file = open('../../../results/%d/water_clusters_pass_%d.txt'%(self.id,self.magi), 'w')
        for c in self.master:
            demo.append(len(c))
        for i in range(maxwater, minwater-1, -1):
            print "Cluster with %d waters: %d" % (i, demo.count(i))
            if self.magi==0:
                self.water_table.append(demo.count(i))
            else:
                self.water_table_post.append(demo.count(i))
            file.write("Cluster with %d waters: %d\n" % (i, demo.count(i)))
        print 'Waters grouped into %d groups' % len(self.master)
        file.write('Waters grouped into %d groups\n' % len(self.master))
        file.close()
        #self.newgrouporg(4.5)


    def newgroup(self, max_err):
        self.master=[]
        done = 0
        self.magi +=1
        pool = []
        print len(self.waters)
        pool.extend(self.waters)
        maxsize=len(self.waters)
        random.shuffle(pool)
        candidatelist = []
        candidate = []
        ties = []
        start=time.time()
        while not done:
            candidatelist=[]
            candidate=[]
            for i in pool:
                candidatewater = i
                candidatelist.append(self.proximal_waters(candidatewater.position(), max_err))
            largest = 0 
            #progressbar(maxsize-len(pool),maxsize, "Processing waters: ")
            for i in candidatelist:
                if len(i) == largest:
                    ties.append(i)
                if len(i) > largest:
                    largest = len(i)
                    ties = []
                    ties.append(i)
            bestcluster = []
            bestrmsd = 999
            clustercounter=0
            removecount=0
            while len(ties)>=1 and len(pool)>=1:
                #print len(ties)
                clustercounter+=1
                bestcluster=[]
                bestrmsd=999
                for i in ties:
                    tempcluster = []
                    tempcluster.extend(i)
                    temp = Cluster()
                    #i.pop(0)
                    for j in i:
                        temp.append(j)
                    if(bestrmsd > temp.std_dev()):
                        bestcluster = temp
                        bestrmsd = temp.std_dev()
                candidate = bestcluster
                if(len(candidate) == 0):
                    candidate.append(pool[0])

                finalflag=1
                while finalflag==1:
                    for i in ties:
                        flag=1
                        if flag==1:
                            if candidate[0] in i:
                                ties.remove(i)
                            else:
                                flag=0
                    finalflag=0
                    for i in ties:
                        if candidate[0] in i:
                            finalflag=1

                for i in ties:
                    if candidate[0] in i:
                        print "ummmmm..."
                """
                for i in ties:
                    if candidate[0] in i:
                        try:
                            if candidate[0]['line num']==3491:
                                for j in i:
                                    print j
                                print "---"
                            ties.remove(i)      
                        except:
                            raw_input("Errored.")

                for i in ties:
                    if candidate[0] in i:
                       ties.remove(i)
                for i in ties:
                    if candidate[0] in i:
                       ties.remove(i)
                for i in ties:
                    if candidate[0] in i:
                        print "Huh."
                """
                
                if candidate[0]['line num']==3491:
                    for i in ties:
                        if candidate[0] in i:
                            for j in i:
                                print j
                            print "oh shit"
                newcluster = Cluster(candidate[0])
                try:
                    #print candidate[0]
                    pool.remove(candidate[0])
                    removecount+=1
                except:
                    print "ERROR ERROR ERROR"
                    print candidate[0].pdb
                    print candidate[0]
                    raw_input("THERE WAS AN ERROR")
                    for i in candidate:
                        print i
                    raw_input("There's the rest of the candidatecluster...")
                    for i in self.master:
                        if candidate[0] in i:
                            for j in i:
                                print j
                    #for i in candidate:
                        #print i
                    print "And um, there's the cluster that was already written out?"
                for j in self.wList:
                    if candidate[0] in j:
                        j.remove(candidate[0])
                candidate.pop(0)
                nukecount=0
                for i in candidate:
                    #print i
                    pool.remove(i)
                    removecount+=1
                    newcluster.append(i)
                    finalflag=1
                    while finalflag==1:
                        for j in ties:
                            flag=1
                            if flag==1:
                                if i in j:
                                    ties.remove(j)
                                else:
                                    flag=0
                        finalflag=0
                        for j in ties:
                            if i in j:
                                finalflag=1


                    for j in self.wList:
                        if i in j:
                            j.remove(i)
                #raw_input("")
                #print "nuked %d"%nukecount
                #print len(newcluster)
                #print "Appending cluster: %s"%newcluster
                self.master.append(newcluster)
                #print newcluster.avg_b()
            if len(pool) < 1:
                done = 1
            print "Round complete. %d Next round."%clustercounter
            print "Number of waters ungrouped = %d"%len(pool)
            print "Number or waters I should have deleted: %d"%removecount
        self.master.sort(Cluster.cmp)
        self.renumber_clusters()
        self.sortthis()
        maxwater = len(self.master[0])
        minwater = len(self.master[-1])
        demo = []
        self.master_len=maxwater
        if self.magi==0:
            self.water_table=[]
            self.water_table_post=[]
        file = open('../../../results/%d/water_clusters_pass_%d.txt'%(self.id,self.magi), 'w')

        for c in self.master:
            demo.append(len(c))
        for i in range(maxwater, minwater-1, -1):
            print "Cluster with %d waters: %d" % (i, demo.count(i))
            if self.magi==0:
                self.water_table.append(demo.count(i))
            else:
                self.water_table_post.append(demo.count(i))
            file.write("Cluster with %d waters: %d\n" % (i, demo.count(i)))
        print 'Waters grouped into %d groups' % len(self.master)
        file.write('Waters grouped into %d groups\n' % len(self.master))
        file.close()
        print time.time()-start
        self.newgrouporg2(4.5)

    def newgrouporg2(self, max_err):
        max_err=4.5
        print "Organic Cutoff is set to 4.5 Angstroms. For this version, contact Brad to change."
        print "Org groupings"
        if len(self.organiclist)==0:
            return
        print len(self.organiclist)
        self.master_org=[]
        done = 0
        self.magi2 +=1
        pool = []
        pool.extend(self.organiclist)
        while not done:
            #print "%d Organics remaining"%len(pool)
            random.shuffle(pool)
            candidatelist = []
            candidate = []
            ties = []
            for i in pool:
                candidatewater = i
                candidatelist.append(self.proximal_organics(candidatewater.position(), max_err))
            largest = 0
            for i in candidatelist:
                if len(i) == largest:
                    ties.append(i)
                if len(i) > largest:
                    largest = len(i)
                    ties = []
                    ties.append(i)
            bestcluster = []
            bestrmsd = 999
            for i in ties:
                tempcluster = []
                tempcluster.extend(i)
                temp = Ocluster(i[0])
                i.pop(0)
                for j in i:
                    temp.append(j)
                if(bestrmsd > temp.std_dev()):
                    bestcluster = temp
                    bestrmsd = temp.std_dev()
            candidate = bestcluster
            if(len(candidate) == 0):
                candidate.append(pool[0])
            newcluster = Ocluster(candidate[0])
            for j in self.oList:
                if candidate[0] in j:
                    j.remove(candidate[0])
            pool.remove(candidate[0])
            candidate.pop(0)
            for i in candidate:
                newcluster.append(i)
                #print i
                pool.remove(i)
                for j in self.oList:
                    if i in j:
                        j.remove(i)
            self.master_org.append(newcluster)
            if len(pool) < 1:
                done = 1
            #print "Round complete. Number of waters ungrouped = %d"%len(pool)
        self.master_org.sort(Ocluster.cmp)
        self.renumber_orgclusters()
        self.sortthis()
        maxwater = len(self.master_org[0])
        minwater = len(self.master_org[-1])
        demo = []
        self.master_len_org=maxwater
        if self.magi2==0:
            self.org_table=[]
            self.org_table_post=[]
        file = open('../../../results/%d/org_clusters_pass_%d.txt'%(self.id,self.magi), 'w')
        for c in self.master_org:
            demo.append(len(c))
        for i in range(maxwater, minwater-1, -1):
            print "Cluster with %d organics: %d" % (i, demo.count(i))
            if self.magi2==0:
                self.org_table.append(demo.count(i))
            else:
                self.org_table_post.append(demo.count(i))
            file.write("Cluster with %d organics: %d\n" % (i, demo.count(i)))
        print 'Organics grouped into %d groups' % len(self.master_org)
        file.write('Organics grouped into %d groups\n' % len(self.master_org))
        file.close()

    def write_master(self):
        self.findoutliers1()
        print "writing output files..."
        user = shell('echo $USER')
        date = datetime.datetime.now()

        file = open(self.master_path, 'w')
        n_pdbs = len(self.pdbs)
        for cluster in self.master:
            cluster.pdbs = [atom.pdb for atom in cluster]
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
                        background-color: white;
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
        for i, pdb in enumerate(self.pdbs):
            file.write("""
                        <tr>
                        <td class='file_n'><pre>%3d  </pre>
                        <td class='filename' id='file%d'>%s""" % (i + 1, i, pdb.shortname))
        file.write('</table>\n')
                
        #header
        file.write("""
                <table>""")
        file.write("""
                <tr>
                <th class='res_num'>Res Num
                <th class='coor' colspan=3>Average Position
                <th class='rmsd'>RMSD
                <th class='rmsd'>Avg B.
                <th class='rmsd'>Sig. B.     
                <th class='file_n' colspan=""" + str(n_pdbs) + """>Files
                <th class='n_files'>#files""")
        #table
        for cluster in self.master:
            file.write("""
                        <tr class='cluster' onclick="document.location='#%d'">
                        <td class='res_num'><a name='top%d'></a>%d
                        <td class='coor'>%.3f<td class='coor'>%.3f<td class='coor'>%.3f
                        <td class='rmsd'>%s
                        <td class='rmsd'>%.3f
                        <td class='rmsd'>%.3f""" % tuple([cluster.res_num] * 3 + cluster.mean() + [cluster.rmsd_str()] + [cluster.avg_b()] + [cluster.sig_b()]))
            is_close = dict([[atom.pdb.filename, atom.distance_from(cluster.mean(), self.err)] for atom in cluster])
            n_matches = [0] * len(self.pdbs)
            o_matches = [0] * len(self.pdbs)
            for atom in cluster:
                n_matches[atom.pdb.number] += 1
                if atom.isoutlier:
                    o_matches[atom.pdb.number] = 1
                        
            for i, pdb in enumerate(self.pdbs):
                file.write("""
                                <td class='file_n' onMouseOver='showFilename(%d,%d)' onMouseOut='clearInfo(%d)'>""" % (i, cluster.res_num, cluster.res_num))
                if n_matches[i]:
                    #if(n_matches[i] > 1 or not is_close[pdb.filename]):
                        #file.write("*")
                    if(o_matches[i]):
                        file.write("<font color=red>")
                    file.write("%d" % (i + 1))
                                        
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
                        """ + "<td class='coor'>%.3f" * 3 + """
                        <td class='rmsd'>%s
                        <tr>
                        <th class='filename' colspan=2>File
                        <th> Water #
                        <th class='coor' colspan=3> Position
                        <th class='rmsd'> Distance""") % tuple([cluster.res_num] + cluster.mean() + [cluster.rmsd_str()]))
            for atom in cluster:
                file.write(("""
                                <tr>
                                <td class='filename'>%s:<td class='file_n'>%d<td>%d&nbsp;
                                """ + "<td class='coor'>%.3f" * 3 + """
                                <td class='rmsd'>%.3f""") % ((atom.pdb.shortname, atom.pdb.number + 1, int(atom.ores)) + atom.position() + (atom.distance_from(cluster.mean()),)))
                if(atom.isoutlier > 0):
                    if atom.isoutlier == 1:
                        file.write("<td>OUTLIER (%d coordinate)" % atom.isoutlier)
                    else:
                        file.write("<td>OUTLIER (%d coordinates)" % atom.isoutlier)
            file.write("""
                        </table>""")
        file.write("""
                </body>
                </html>""")
        self.write_orgmaster()

    def write_orgmaster(self):
        user = shell('echo $USER')
        date = datetime.datetime.now()

        file = open(self.orgmaster_path, 'w')
        n_pdbs = len(self.pdbs)
        for cluster in self.master_org:
            cluster.pdbs = [atom.pdb for atom in cluster]
        file.write("""
                <html>
                <head>
                <title>Organic Consensus List</title>
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
                        background-color: white;
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
        file.write("<p>Allowable error began at <b>%.2f</b> A and was capped at <b>%.2f</b> A.</p>\n" % (self.start_err, self.orgerr-self.increment))
        #files
        file.write("""
                <table>
                <tr>
                <th colspan=2>PDB Files""")
        for i, pdb in enumerate(self.pdbs):
            file.write("""
                        <tr>
                        <td class='file_n'><pre>%3d  </pre>
                        <td class='filename' id='file%d'>%s""" % (i + 1, i, pdb.shortname))
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
        for cluster in self.master_org:
            file.write("""
                        <tr class='cluster' onclick="document.location='#%d'">
                        <td class='res_num'><a name='top%d'></a>%d
                        <td class='coor'>%.3f<td class='coor'>%.3f<td class='coor'>%.3f
                        <td class='rmsd'>%s""" % tuple([cluster.res_num] * 3 + cluster.mean() + [cluster.rmsd_str()]))
            is_close = dict([[atom.pdb.filename, atom.distance_from(cluster.mean(), self.err)] for atom in cluster])
            n_matches = [0] * len(self.pdbs)
            o_matches = [0] * len(self.pdbs)
            for atom in cluster:
                n_matches[atom.pdb.number] += 1
                if atom.isoutlier:
                    o_matches[atom.pdb.number] = 1
                        
            for i, pdb in enumerate(self.pdbs):
                file.write("""
                                <td class='file_n' onMouseOver='showFilename(%d,%d)' onMouseOut='clearInfo(%d)'>""" % (i, cluster.res_num, cluster.res_num))
                if n_matches[i]:
                    #if(n_matches[i] > 1 or not is_close[pdb.filename]):
                        #file.write("*")
                    if(o_matches[i]):
                        file.write("<font color=red>")
                    file.write("%d" % (i + 1))
                                        
            file.write("""
                        <td class='n_files'>(%d)
                        <td id='info%d' class='filename' width='400px'>""" % (len(cluster), cluster.res_num))
                        
        file.write("""
                </table>
                <table>""")
        for cluster in self.master_org:
            file.write("""
                        <a name='%d'><h1>%d</h1></a>""" % (cluster.res_num, cluster.res_num))
            file.write(("""
                        <table>
                        <tr class='cluster' onclick="document.location='#top%d'">
                        <th colspan=3>Average
                        """ + "<td class='coor'>%.3f" * 3 + """
                        <td class='rmsd'>%s
                        <tr>
                        <th class='filename' colspan=2>File
                        <th> Organic #
                        <th class='coor' colspan=3> Position
                        <th class='rmsd'> Distance""") % tuple([cluster.res_num] + cluster.mean() + [cluster.rmsd_str()]))
            for atom in cluster:
                file.write(("""
                                <tr>
                                <td class='filename'>%s:<td class='file_n'>%d<td>%d&nbsp;
                                """ + "<td class='coor'>%.3f" * 3 + """
                                <td class='rmsd'>%.3f""") % ((atom.pdb.shortname, atom.pdb.number + 1, int(atom.ores)) + atom.position2() + (atom.distance_from(cluster.mean()),)))
            file.write("""
                        </table>""")
        file.write("""
                </body>
                </html>""")

    def findoutliers1(self):
        return
        outliers = []
        critvalues = [0, 0, 0, .970, .829, .71, .625, .568, .615, .570, .534, .625, .592, .565, .590, .568, .548, .531, .516, .503, .491, .48, .47, .461, .452, .445, .438, .432, .426, .149, .414]
        for cluster in self.master:
            for i in outliers:
                i.isoutlier = i.isoutlier + 1
            outliers = []
            tempcluster = sorted(cluster, key=lambda atom: atom['x'])
            clustersize = len(tempcluster)
            if(clustersize < 3):
                continue
                #print "Cluster too small for statistical analysis"
            if(clustersize >= 3 and clustersize <= 7):
                #print critvalues[clustersize]
                #print "Use r10 test"
                #print "Size %d"%clustersize
                x2 = tempcluster[1]['x']
                x1 = tempcluster[0]['x']
                xn = tempcluster[clustersize-1]['x']
                xn1 = tempcluster[clustersize-2]['x']
                if (x2-x1) / (xn-x1) > critvalues[clustersize] and (xn-x1)!=0:
                    #  print "Critical Value 1x Fails"
                        if not tempcluster[0] in outliers:
                            outliers.append(tempcluster[0])
                if (xn-xn1) / (xn-x1) > critvalues[clustersize] and (xn-x1)!=0:
                    # print "Critical Value 2x Fails"
                        if not tempcluster[clustersize-1] in outliers:
                            outliers.append(tempcluster[0])
                tempcluster = sorted(cluster, key=lambda atom: atom['y'])
                x2 = tempcluster[1]['y']
                x1 = tempcluster[0]['y']
                xn = tempcluster[clustersize-1]['y']
                xn1 = tempcluster[clustersize-2]['y']
                if (x2-x1) / (xn-x1) > critvalues[clustersize] and (xn-x1)!=0:
                    #  print "Critical Value 1y Fails"
                        if not tempcluster[0] in outliers:
                            outliers.append(tempcluster[0])
                if (xn-xn1) / (xn-x1) > critvalues[clustersize] and (xn-x1)!=0:
                    #  print "Critical Value 2y Fails"
                        if not tempcluster[clustersize-1] in outliers:
                            outliers.append(tempcluster[0])
                tempcluster = sorted(cluster, key=lambda atom: atom['z'])
                x2 = tempcluster[1]['z']
                x1 = tempcluster[0]['z']
                xn = tempcluster[clustersize-1]['z']
                xn1 = tempcluster[clustersize-2]['z']
                if (x2-x1) / (xn-x1) > critvalues[clustersize] and (xn-x1)!=0:
                    #  print "Critical Value 1z Fails"
                        if not tempcluster[0] in outliers:
                            outliers.append(tempcluster[0])
                if (xn-xn1) / (xn-x1) > critvalues[clustersize]:
                    #print "Critical Value 2z Fails"
                    if not tempcluster[clustersize-1] in outliers and (xn-x1)!=0:
                        outliers.append(tempcluster[0])
            if(clustersize >= 8 and clustersize <= 10):
                #print critvalues[clustersize]
                #print "Use r11 test"
                #print "Size %d"%clustersize
                x2 = tempcluster[1]['x']
                x1 = tempcluster[0]['x']
                xn = tempcluster[clustersize-1]['x']
                xn1 = tempcluster[clustersize-2]['x']
                if (x2-x1) / (xn1-x1) > critvalues[clustersize] and (xn1-x1)!=0:
                    # print "Critical Value 1x Fails"
                        if not tempcluster[0] in outliers:
                            outliers.append(tempcluster[0])
                if (xn-xn1) / (xn-x2) > critvalues[clustersize] and (xn-x2)!=0:
                    #  print "Critical Value 2x Fails"
                        if not tempcluster[clustersize-1] in outliers:
                            outliers.append(tempcluster[0])
                tempcluster = sorted(cluster, key=lambda atom: atom['y'])
                x2 = tempcluster[1]['y']
                x1 = tempcluster[0]['y']
                xn = tempcluster[clustersize-1]['y']
                xn1 = tempcluster[clustersize-2]['y']
                if (x2-x1) / (xn1-x1) > critvalues[clustersize] and (xn1-x1)!=0:
                    #  print "Critical Value 1y Fails"
                        if not tempcluster[0] in outliers:
                            outliers.append(tempcluster[0])
                if (xn-xn1) / (xn-x2) > critvalues[clustersize] and (xn-x2)!=0:
                    #  print "Critical Value 2y Fails"
                        if not tempcluster[clustersize-1] in outliers:
                            outliers.append(tempcluster[0])
                tempcluster = sorted(cluster, key=lambda atom: atom['z'])
                x2 = tempcluster[1]['z']
                x1 = tempcluster[0]['z']
                xn = tempcluster[clustersize-1]['z']
                xn1 = tempcluster[clustersize-2]['z']
                if (x2-x1) / (xn1-x1) > critvalues[clustersize] and (xn1-x1)!=0:
                    #  print "Critical Value 1z Fails"
                        if not tempcluster[0] in outliers:
                            outliers.append(tempcluster[0])
                if (xn-xn1) / (xn-x2) > critvalues[clustersize] and (xn-x2)!=0:
                    #   print "Critical Value 2z Fails"
                        if not tempcluster[clustersize-1] in outliers:
                            outliers.append(tempcluster[0])
            if(clustersize >= 11 and clustersize <= 13):
                #print critvalues[clustersize]
                #print "Use r21 test"
                #print "Size %d"%clustersize
                x3 = tempcluster[2]['x']
                x2 = tempcluster[1]['x']
                x1 = tempcluster[0]['x']
                xn = tempcluster[clustersize-1]['x']
                xn1 = tempcluster[clustersize-2]['x']
                xn2 = tempcluster[clustersize-3]['x']
                if (x3-x1) / (xn1-x1) > critvalues[clustersize] and (xn1-x1)!=0:
                    # print "Critical Value 1x Fails"
                        if not tempcluster[0] in outliers:
                            outliers.append(tempcluster[0])
                if (xn-xn2) / (xn-x2) > critvalues[clustersize] and (xn-x2)!=0:
                    #   print "Critical Value 2x Fails"
                        if not tempcluster[clustersize-1] in outliers:
                            outliers.append(tempcluster[0])
                tempcluster = sorted(cluster, key=lambda atom: atom['y'])
                x3 = tempcluster[2]['y']
                x2 = tempcluster[1]['y']
                x1 = tempcluster[0]['y']
                xn = tempcluster[clustersize-1]['y']
                xn1 = tempcluster[clustersize-2]['y']
                xn2 = tempcluster[clustersize-3]['y']
                if (x3-x1) / (xn1-x1) > critvalues[clustersize] and (xn1-x1)!=0:
                    # print "Critical Value 1y Fails"
                        if not tempcluster[0] in outliers:
                            outliers.append(tempcluster[0])
                if (xn-xn2) / (xn-x2) > critvalues[clustersize] and (xn-x2)!=0:
                    # print "Critical Value 2y Fails"
                        if not tempcluster[clustersize-1] in outliers:
                            outliers.append(tempcluster[0])
                tempcluster = sorted(cluster, key=lambda atom: atom['z'])
                x3 = tempcluster[2]['z']
                x2 = tempcluster[1]['z']
                x1 = tempcluster[0]['z']
                xn = tempcluster[clustersize-1]['z']
                xn1 = tempcluster[clustersize-2]['z']
                xn2 = tempcluster[clustersize-3]['z']
                if (x3-x1) / (xn1-x1) > critvalues[clustersize] and (xn1-x1)!=0:
                    #  print "Critical Value 1z Fails"
                        if not tempcluster[0] in outliers:
                            outliers.append(tempcluster[0])
                if (xn-xn2) / (xn-x2) > critvalues[clustersize] and (xn-x2)!=0:
                    #  print "Critical Value 2z Fails"
                        if not tempcluster[clustersize-1] in outliers:
                            outliers.append(tempcluster[0])

            if(clustersize >= 14 and clustersize <= 30):
                # print critvalues[clustersize]
                    #print "Use r22 test"
                # print "Size %d"%clustersize
                    x3 = tempcluster[2]['x']
                    x2 = tempcluster[1]['x']
                    x1 = tempcluster[0]['x']
                    xn = tempcluster[clustersize-1]['x']
                    xn1 = tempcluster[clustersize-2]['x']
                    xn2 = tempcluster[clustersize-3]['x']
                    if (x3-x1) / (xn2-x1) > critvalues[clustersize] and (xn2-x1)!=0:
                        # print "Critical Value 1x Fails"
                            if not tempcluster[0] in outliers:
                                outliers.append(tempcluster[0])
                    if (xn-xn2) / (xn-x3) > critvalues[clustersize] and (xn-x3)!=0:
                        #  print "Critical Value 2x Fails"
                            if not tempcluster[clustersize-1] in outliers:
                                outliers.append(tempcluster[0])
                    tempcluster = sorted(cluster, key=lambda atom: atom['y'])
                    x3 = tempcluster[2]['y']
                    x2 = tempcluster[1]['y']
                    x1 = tempcluster[0]['y']
                    xn = tempcluster[clustersize-1]['y']
                    xn1 = tempcluster[clustersize-2]['y']
                    xn2 = tempcluster[clustersize-3]['y']
                    if (x3-x1) / (xn2-x1) > critvalues[clustersize] and (xn2-x1)!=0:
                        #  print "Critical Value 1y Fails"
                            if not tempcluster[0] in outliers:
                                outliers.append(tempcluster[0])
                    if (xn-xn2) / (xn-x3) > critvalues[clustersize] and (xn-x3)!=0:
                        # print "Critical Value 2y Fails"
                            if not tempcluster[clustersize-1] in outliers:
                                outliers.append(tempcluster[0])
                    tempcluster = sorted(cluster, key=lambda atom: atom['z'])
                    x3 = tempcluster[2]['z']
                    x2 = tempcluster[1]['z']
                    x1 = tempcluster[0]['z']
                    xn = tempcluster[clustersize-1]['z']
                    xn1 = tempcluster[clustersize-2]['z']
                    xn2 = tempcluster[clustersize-3]['z']
                    if (x3-x1) / (xn2-x1) > critvalues[clustersize] and (xn2-x1)!=0:
                        #print "Critical Value 1z Fails"
                        if not tempcluster[0] in outliers:
                            outliers.append(tempcluster[0])
                    if (xn-xn2) / (xn-x3) > critvalues[clustersize] and (xn-x3)!=0:
                        # print "Critical Value 2z Fails"
                            if not tempcluster[clustersize-1] in outliers:
                                outliers.append(tempcluster[0])

    def phase3(self):
        temp = []
        self.magi=-1
        self.magi2=-1
        for pdb in self.pdbs:
            if(pdb.myname.find("PRESUPER")!=-1 or 1):
                temp.append(pdb)
        self.pdbs=temp
        for pdb in self.pdbs:
            pdb.findsymms()
        self.createlist()
        self.newgroup(1.4)

        #This section runs through symmetry related molecules and figures out the best cluster.
        for pdb in self.pdbs:
            for i in pdb.tolist:
                bestfit=999
                bestorg=None
                toupdate=None
                for atom in pdb.tolist[i]:
                    if atom.chain=='O':
                        toupdate=atom
                    for cluster in self.master_org:
                        if cluster.estimate_fit(atom,4.5):
                            if cluster.res_num<bestfit:
                                bestfit=cluster.res_num
                                bestorg=atom
                toupdate.optimum_update(bestorg)
            for i in pdb.twlist:
            #for i in progressbar(pdb.twlist, "Processing Waters..."):
                bestfit=999
                bestwater=None
                toupdate=None
                for atom in pdb.twlist[i]:
                    if atom['chain']=='W':
                        toupdate=atom
                    for cluster in self.master:
                        if cluster.estimate_fit(atom,1.3):
                            if cluster.res_num<bestfit:
                                bestfit=cluster.res_num
                                bestwater=atom
                if toupdate!=None and bestwater!=None:
                    toupdate.optimum_update(bestwater.position())
        #Now recheck the ordering
        self.createlist2()
        self.newgroup(1.4)

        waterclusterpdb = PDB('Renumbered/clusters.pdb')
        orgclusterpdb = PDB('Renumbered/orgcluster.pdb')
        clusterline = 'ATOM   1052  O   WAT C 312     -91.585  -9.581  16.868  1.00 55.71      O    O\n'
        clusterline1 = 'ATOM   1052  O   ORG C 312     -91.585  -9.581  16.868  1.00 55.71      O    O\n'
        for cluster in self.master:
            temp = Atom(clusterline, cluster.res_num, waterclusterpdb)
            temp['res num'] = cluster.res_num
            temp['x'] = float('%.3f' % cluster.mean()[0])
            temp['y'] = float('%.3f' % cluster.mean()[1])
            temp['z'] = float('%.3f' % cluster.mean()[2])
            temp['B'] = float('%.2f' % cluster.avg_b())
            waterclusterpdb.append(temp)
        for cluster in self.master_org:
            temp = Atom(clusterline1, cluster.res_num, orgclusterpdb)
            temp['res num'] = cluster.res_num
            temp['x'] = float('%.3f' % cluster.mean()[0])
            temp['y'] = float('%.3f' % cluster.mean()[1])
            temp['z'] = float('%.3f' % cluster.mean()[2])
            orgclusterpdb.append(temp)
        waterclusterpdb.write(self.id)
        orgclusterpdb.write(self.id)
        #And write to file.
        self.write_master()
        for pdb in self.pdbs:
            pdb.write(self.id,2)

    def viewgraph(self):
        self.water_table.reverse()
        self.water_table_post.reverse()
        N = self.master_len
        Before = self.water_table
        After = self.water_table_post
        ind = np.arange(N)  # the x locations for the groups
        width = 0.35       # the width of the bars


        plt.subplot(111)
        print ind
        rects1 = plt.bar(ind, Before, width, color='r')
        rects2 = plt.bar(ind+width, After, width, color='b')
        ind2=[]
        for i in ind:
            ind2.append(i+1)
        plt.ylabel('Number of clusters')
        plt.title('Water Analysis')
        plt.xlabel('Cluster size')
        plt.xticks(ind+width, ind2 )
        plt.legend( (rects1[0], rects2[0]), ('Before', 'After') )

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                        ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        plt.savefig("%s/watercluster.png"%self.root,dpi=600,format='png')
        plt.savefig("%s/watercluster.eps"%self.root,dpi=600,format='eps')
        plt.show()
        #plt.savefig("watercluster.png",format='png')

        #self.viewgraph2()
        
    def viewgraph2(self):
        return
        self.org_table.reverse()
        self.org_table_post.reverse()
        N = self.master_len_org
        Before = self.org_table
        After = self.org_table_post

        ind = np.arange(N)  # the x locations for the groups
        width = 0.35       # the width of the bars


        plt.subplot(111)
        rects1 = plt.bar(ind, Before, width, color='r')
        rects2 = plt.bar(ind+width, After, width, color='b')
        ind2=[]
        for i in ind:
            ind2.append(i+1)
        plt.ylabel('Number of clusters')
        plt.title('Organic Solvent Analysis')
        plt.xlabel('Cluster size')
        plt.xticks(ind+width, ind2 )
        plt.legend( (rects1[0], rects2[0]), ('Before', 'After') )

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                        ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        plt.savefig("%s/organiccluster.png"%self.root,dpi=600,format='png')
        plt.savefig("%s/organiccluster.eps"%self.root,dpi=600,format='eps')
        plt.show()        
    
def run():
    #iprint "Preprocessing files. Please wait."
    print "FINAL ROUND"
    argv = sys.argv[1:]
    id=argv[0]
    root = 'Renumbered/'
    if(root[-1:] != '/'):
        root += '/'
    start_err = '1.0'
    if(not os.path.exists('../../../results/%d'%int(id))):
        os.makedirs('../../../results/%d'%int(id))
    url = 'http://129.10.89.145/running.php?job=%d&status=400'%int(id)
    raw_return=urllib.urlopen(url).read()

    pdb_filenames = []
    filenames = os.listdir(os.getcwd())
    for f in filenames:
        if(f[-4:] == '.pdb'):
            pdb_filenames.append(f)
    #print len(pdb_filenames)
    a = Analyzer(pdb_filenames, root, int(id), err=start_err)
    input = ''
    a.phase3()
    """
    try:
        a.phase3()
    except:
        url='http://129.10.89.145/running.php?job=%d&status=322'%int(id)
        raw_return=urllib.urlopen(url).read()
        print "Exploding."
        return"""
    #a.viewgraph()
    url = 'http://129.10.89.145/running.php?job=%d&status=777'%int(id)
    raw_return=urllib.urlopen(url).read()
    os.chdir('../../../results/%d'%int(id))
    filenames= os.listdir(os.getcwd())
    zf = zipfile.ZipFile('results.zip', 'w', zipfile.ZIP_DEFLATED)
    for f in filenames:
        zf.write(f)
        os.system('rm -rf %s'%f)
    zf.close()
    return
if(__name__ == '__main__'):
    run()
        
        
