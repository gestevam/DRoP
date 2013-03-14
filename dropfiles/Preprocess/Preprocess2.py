#!/usr/bin/python
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
import pp

ppservers = ()

# Creates jobserver with automatically detected number of workers
job_server = pp.Server(2, ppservers=ppservers)
#job_server = pp.Server(6, ppservers=ppservers)

print "Starting pp with", job_server.get_ncpus(), "workers"

def progressbar(it, prefix = "", size = 60):
    count = len(it)
    def _show(_i):
        x = int(size*_i/count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), _i, count))
        sys.stdout.flush()
    
    _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()

def shell(cmd):
    return -1

def myjob(a,w):
    symmwaters = a.varpass(w)
    optimum = [w.position()[0], w.position()[1], w.position()[2], 'x,y,z', [0, 0, 0]]
    optimumcount = w.howclose()
    changemade = 0
    goodcheck=[]
    for j in symmwaters:
        for i in j:
            checkcount = 0
            checkcount = w.pdb.compare(i)
            if checkcount>0 and notsame(i,optimum):
                goodcheck.append(i)
            
            """if(len(w.pdb.findneighbor(i,w['res num']))>0):
                print "SYMMETRY"
                flagger+=1
                t0 = "ATOM    957  O   HOH B   1      36.504 -10.582  -2.929  1.00 13.36      A    O"
                t1 = w['res num']
                t2 = w.pdb
                temp = Atom(t0, t1, t2)
                temp['x'] = i[0]
                temp['y'] = i[1]
                temp['z'] = i[2]
                temp['res num']=w['res num']
                #temp['B']=float("%.2d"%flagger)
                temp['chain']='S'
                w.pdb.append(temp)"""
            if checkcount > optimumcount and i in goodcheck:
                goodcheck.append(optimum)
                goodcheck.remove(i)
                optimumcount = checkcount
                optimum = i
                changemade = 1
    #print count+170
    return(goodcheck,optimum)
    #print w


class Cluster(list):
    def __init__(self, atom):
        list.__init__(self)
        self.sum = [0.] * 3
        self.a_sum = 0
        self.b_sum = 0
        self.c_sum = 0
        self.a = 0
        self.b = 0
        self.c = 0
        self.res_num = None
        self.append(atom)
    def append(self, atom):
        list.append(self, atom)
        self.a_sum += float(atom.a)
        self.b_sum += float(atom.b)
        self.c_sum += float(atom.c)
        self.a = self.a_sum / len(self)
        self.b = self.b_sum / len(self)
        self.c = self.c_sum / len(self)
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
        self.a_sum = 0
        self.b_sum = 0
        self.c_sum = 0
        self.a = 0
        self.b = 0
        self.c = 0
        self.res_num = None
        self.append(atom)
    def append(self, atom):
        list.append(self, atom)
        self.a_sum += float(atom.a)
        self.b_sum += float(atom.b)
        self.c_sum += float(atom.c)
        self.a = self.a_sum / len(self)
        self.b = self.b_sum / len(self)
        self.c = self.c_sum / len(self)
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
            atom['res num'] = res_num
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
            self.append(Cluster(atom))
                
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
                        

    def __init__(self, pdb_filenames, root, err=1):
        self.pdbs = []
        totalnum = 0
        for filename in pdb_filenames:
            self.pdbs.append(PDB(filename, root + filename.split('/')[-1],watercheck=1))
        self.pdbs.sort(key=str)
        for i, pdb in enumerate(self.pdbs):
            pdb.number = i
            pdb.shortname = pdb.filename.split('/')[-1]
            totalnum = i
        self.waters = []
        self.aa = []
        self.organics = []
        self.wList = []
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
            for atom in pdb:
                if(atom['type'] == "ATOM" or atom['type'] == "HETATM"):
                    if(atom['res name'] in water_names):
                        self.waters.append(atom)
                    if(atom['res name'] in protein_names):
                        self.aa.append(atom)
                    if(atom['res name'] in organic_names):
                        self.organics.append(atom)
                                    
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
            #print "Calculating nearby contacts for waters."
            for w in self.waters:
                count = count + 1
                for pdb in self.pdbs:
                    if (pdb == w.pdb):
                        w.setclose(pdb.compare(w.position()))
            
            for o in self.organics:
                for pdb in self.pdbs:
                    if (pdb == o.pdb):
                        o.setclose(pdb.compare(o.position()))
        self.root = root + self.stamp
        if(not os.path.exists(self.root)):
            os.makedirs(self.root)
        self.master = Analyzer.Cluster_List()
        self.master_org = Analyzer.Ocluster_List()
        self.master_path = self.root + 'master.html'
        self.orgmaster_path = self.root + 'org.html'
        self.err = self.start_err = 1.0
        self.orgerr = 1.0
        self.centers = []

    def notsame(check, base):
        dx= check[0]-base[0]
        dy= check[1]-base[1]
        dz= check[2]-base[2]
        if dx**2+dy**2+dz**2 < 0.1:
            return 0
        else:
            return 1
        
        print "ABORT"
        sys.exit(1)




    def optimize(self):
        a = symgen.symgen()
        symwaters = []
        optimum = []
        original = []
        originalcount = 0
        optimumcount = 0
        newx = 0
        newy = 0
        newz = 0
        verbose = 0
        numwater = float(len(self.waters))
        count = 0
        counter = 0
        goodcheck=[]
        print "Optimizing individual water symmetries - Please wait."
        file = open(self.root + 'optimize.log', 'w')
        print "%d total waters."%len(self.waters)
        count=0
        count2=1
        print "HELLO?!"
        jobs = [(w, job_server.submit(myjob,(a,w,), (self.notsame,))) for w in self.waters]
        print "Jobs set."
        for w, job in progressbar(jobs,"Optimizing Water Positions",20):
            temp=job()
            #print "Sum of primes below", input, "is", job()
        
            #temp = job1()
            goodcheck=temp[0]
            optimum=temp[1]
            for i in goodcheck:
                t0 = "ATOM    957  O   HOH B   1      36.504 -10.582  -2.929  1.00 13.36      A    O"
                t1 = w['res num']
                t2 = w.pdb
                temp = Atom(t0, t1, t2)
                temp['x'] = i[0]
                temp['y'] = i[1]
                temp['z'] = i[2]
                temp['res num']=w['res num']
                #temp['B']=float("%.2d"%flagger)
                temp['chain']='S'
                w.pdb.append(temp)
            w.optimum_update(optimum)
            w['chain']='W'
        job_server.destroy()
        file.close()

    def optimize2(self):
        a = symgen.symgen()
        symorganics = []
        processing = []
        optimum = []
        original = []
        originalcount = 0
        optimumcount = 0
        maxcounts = []
        newx = 0
        newy = 0
        newz = 0
        nflag = 0
        verbose = 0
        numorg = float(len(self.organics))
        count = 0
        counter = 0
        checkcounter = 0
        file = open(self.root + 'optimize_organic.log', 'w')
        curres = 0
        flag = 0
        curror = ""
        currch = ""
        currpdb = ""
        hold = ""
        print "Optimizing individual organic/ligand symmetries - Please wait."
        changemade = 0
        for o in self.organics:
            count = count + 1
            counter = counter + 1
            if(counter % 10 == 0):
                disp = float(count / numorg) * 100
            # print "Optimizing individual organic symmetries - %.1f%% complete. "%disp
                counter = 0
            if((o['res num'] == curres) and (o['res name'] == curror) and (o['chain'] == currch)):
                processing.append(o)
                hold = o
            else: #process data and start a new list
                if (flag == 1):
                    changemade = 0
                    hold = o
                    tproc = []
                    tproc.append(o)
                    curres = o['res num']
                    curror = o['res name']
                    currch = o['chain']
                    symmorganics = a.varpass2(processing)
                    opcount = []
                    for i in range(1000):
                        opcount.append(0)
                        best = 0
                        counter = 0
                        bestpos = 0
                    for i in symmorganics:
                        checkcounter = 0
                        for j in i:
                            checkcount = 0
                            for pdb in self.pdbs:
                                if (pdb == currpdb):
                                    #print '---'
                                    #print "%s%s"%(o['res name'],o['res num'])
                                    checkcount = pdb.compare(j)
                            opcount[checkcounter] = opcount[checkcounter] + checkcount
                            checkcounter += 1
                    maxpos = 0
                    mypos = 0
                    maxcount = 0
                    for i in opcount:
                        if(i > maxcount):
                            maxpos = mypos
                            maxcount = i
                        mypos += 1

                    for i in symmorganics:
                        optimum.append(i[maxpos])
                    pcount = 0
                    for i in processing:
                        j = optimum[pcount]
                        if maxcount == 0:
                            file.write(str(i.pdb) + " " + i['res name'] + ' ' + i['atom name'] + " %d No Change Made\n" % i['res num'])
                            file.write("****WARNING**** THIS ATOM MAKES NO PROTEIN CONTACTS ****WARNING****\n\n")
                        else:
                            if((str(j[4]) == "[0, 0, 0]" and j[3] == "x,y,z")):
                                if(verbose):
                                    file.write(str(i.pdb) + " " + i['res name'] + ' ' + i['atom name'] + " %d No Change Made\n\n" % i['res num'])
                            else:
                                file.write(str(i.pdb) + " " + i['res name'] + ' ' + i['atom name'] + " %d Optimization Results" % i['res num'])
                                file.write("\nOriginal Position: %.3f %.3f %.3f" % (i.position()[0], i.position()[1], i.position()[2]))
                                file.write("\nOriginal Contacts: %d" % i.howclose())
                                file.write("\nOptimized Position: %.3f %.3f %.3f" % (j[0], j[1], j[2]))
                                file.write("\nOptimized Symmetry UC: " + str(j[4]))
                                file.write("\nOptimized Operator: " + j[3])
                                file.write("\nOptimized Contacts: %d\n\n" % maxcount)
                        if maxcount > 0:
                            i.optimum_update(j)
                        pcount += 1

                    optimum = []
                    currpdb = o.pdb
                    processing = []
                    processing.append(tproc[0])
                                        
                else:
                    flag = 1
                    optimum = []
                    processing = []
                    processing.append(o)
                    curres = o['res num']
                    curror = o['res name']
                    currch = o['chain']
                    currpdb = o.pdb
        changemade = 0
        o = hold
        symmorganics = a.varpass2(processing)
        opcount = []
        for i in range(1000):
            opcount.append(0)
        for i in symmorganics:
            checkcounter = 0
            for j in i:
                checkcount = 0
                for pdb in self.pdbs:
                    if (pdb == currpdb):
                        checkcount = pdb.compare(j)
                opcount[checkcounter] = opcount[checkcounter] + checkcount
                checkcounter += 1
        maxpos = 0
        mypos = 0
        maxcount = 0
        for i in opcount:
            if(i > maxcount):
                maxpos = mypos
                maxcount = i
            mypos += 1

        for i in symmorganics:
            optimum.append(i[maxpos])
        pcount = 0
        for i in processing:
            j = optimum[pcount]
            if maxcount == 0:
                file.write(str(i.pdb) + " " + i['res name'] + ' ' + i['atom name'] + " %d No Change Made\n" % i['res num'])
                file.write("****WARNING**** THIS ATOM MAKES NO PROTEIN CONTACTS ****WARNING****\n\n")
            else:
                if((str(j[4]) == "[0, 0, 0]" and j[3] == "x,y,z")):
                    if(verbose):
                        file.write(str(i.pdb) + " " + i['res name'] + ' ' + i['atom name'] + " %d No Change Made\n\n" % i['res num'])
                else:
                    file.write(str(i.pdb) + " " + i['res name'] + ' ' + i['atom name'] + " %d Optimization Results" % i['res num'])
                    file.write("\nOriginal Position: %.3f %.3f %.3f" % (i.position()[0], i.position()[1], i.position()[2]))
                    file.write("\nOriginal Contacts: %d" % i.howclose())
                    file.write("\nOptimized Position: %.3f %.3f %.3f]" % (j[0], j[1], j[2]))
                    file.write("\nOptimized Symmetry UC: " + str(j[4]) + ']')
                    file.write("\nOptimized Operator: " + j[3] + ']')
                    file.write("\nOptimized Contacts: %d\n\n" % maxcount)
            if maxcount > 0:
                i.optimum_update(j)
            pcount += 1

        optimum = []
        processing = []
        file.close()
        
    def phase1(self):
        ti1=time.clock()
        print "Optimizing water positions"
        self.optimize()
        #print "Optimizing organic positions"
        #self.optimize2()
        """
        sym=symgen.symgen()
        print "Preprocessing water molecules."
        for w in self.waters:
            w['chain']='W'
            symm=sym.varpass(w)
            flagger=0
            for j in symm:
                for i in j:
                    if(len(w.pdb.findneighbor(i,w['res num']))>0):
                        #print "SYMMETRY"
                        flagger+=1
                        t0 = "ATOM    957  O   HOH B   1      36.504 -10.582  -2.929  1.00 13.36      A    O"
                        t1 = w['res num']
                        t2 = w.pdb
                        temp = Atom(t0, t1, t2)
                        temp['x'] = i[0]
                        temp['y'] = i[1]
                        temp['z'] = i[2]
                        temp['res num']=w['res num']
                        #temp['B']=float("%.2d"%flagger)
                        temp['chain']='S'
                        w.pdb.append(temp)
        """
        ti2=time.clock()
        print ti2-ti1
        print "Preprocessing organic molecules."
        self.phase2()
        for pdb in self.pdbs:
            pdb.write(self.stamp,1)

    def phase2(self):
        #return
        currres=0
        c1l=''
        currname=''
        prevpdb= ''
        newpdblines=[]
        processing=[]
        curres = 0
        flag=0
        curror = ""
        currch = ""
        currpdb = ""
        hold = ""
        symop = symgen.symgen()
        for i in self.organics:
            i['chain']='O'
            if i.pdb != currpdb or i['res num']!=currres or i['chain'] != currch:
                if(currres==0):
                    currpdb=i.pdb
                    prevpdb=i.pdb
                    currres=i['res num']
                    currname=i['res name']
                    currch=i['chain']
                else:
                    currres=i['res num']
                    currname=i['res name']
                    currch=i['chain']
                    for j in newpdblines:
                        prevpdb.append(j)
                    currpdb=i.pdb
                    newpdblines=[]
            if((i['res num'] == curres) and (i['res name'] == curror) and (i['chain'] == currch)):
                processing.append(i)
                hold = i
            else: #process data and start a new list
                if (flag == 1):
                    temp=[]
                    countholder=[]
                    origcontacts=0
                    biggestcount=0
                    keepcount=0
                    docount=0
                    youmu=[]
                    possible=[]                 
                    updatefinally=[]
                    updatefinally=deepcopy(processing)
                    prevpdb=processing[0].pdb
                    derp=[]
                    for i1 in range(-1,2):
                        for j1 in range(-1,2):
                            for k1 in range(-1,2):
                                temp=[]
                                for a in processing:
                                    temp.append(symop.orgsympass(a,i1,j1,k1))
                                for nk in range((len(temp))):
                                    for j in range((len(temp[0]))):
                                            neighbor= processing[nk]
                                            neigh=prevpdb.findneighbor(temp[nk][j],i['res num'])
                                            if len(neigh):
                                                if not nk in youmu:
                                                    youmu.append(nk)
                                                if not j in countholder:
                                                    countholder.append(j)
                                count=-1
                                counter=0
                                for eirin in range(len(temp)):
                                    count+=1
                                    for yuyuko in countholder:
                                        counter+=1
                                        cid='O'
                                        if str(temp[eirin][yuyuko][3])!='x,y,z':
                                            cid='Z'
                                        if cid!='O':
                                            while (len(derp)<counter):
                                                derp.append([])
                                            a=updatefinally[count]
                                            a.optimum_update(temp[eirin][yuyuko])
                                            t0 = "ATOM    957  O   HOH B   1      36.504 -10.582  -2.929  1.00 13.36      A    O"
                                            t1 = curres
                                            t2 = currpdb
                                            tempy = Atom(t0, t1, t2)
                                            tempy['x'] = a['x']
                                            tempy['y'] = a['y']
                                            tempy['z'] = a['z']
                                            tempy['res name']=a['res name']
                                            tempy['res num']=a['res num']
                                            tempy['atom name']=a['atom name']
                                            tempy['chain']=cid
                                            tempy['atype']=a['atype']
                                            tempy['B']=float("%.2d"%count)
                                            #print tempy
                                            derp[counter-1].append(tempy)
                                            #newpdblines.append(tempy)
                                youmu=[]
                                countholder=[] 
                                keepcount=0
                    for peppy in derp:
                        for slippy in peppy:
                            newpdblines.append(slippy)
                    curres = i['res num']
                    curror = i['res name']
                    currch = i['chain']
                    processing=[]
                    processing.append(i)
                else:
                    flag = 1
                    optimum = []
                    processing = []
                    processing.append(i)
                    curres = i['res num']
                    curror = i['res name']
                    currch = i['chain']
                    currpdb = i.pdb
        currpdb=i.pdb
        newpdblines=[]
        temp=[]
        countholder=[]
        origcontacts=0
        biggestcount=0
        keepcount=0
        docount=0
        youmu=[]
        possible=[]                 
        updatefinally=[]
        updatefinally=deepcopy(processing)
        prevpdb=processing[0].pdb
        derp=[]
        for i1 in range(-1,2):
            for j1 in range(-1,2):
                for k1 in range(-1,2):
                    temp=[]
                    for a in processing:
                        temp.append(symop.orgsympass(a,i1,j1,k1))
                    for nk in range((len(temp))):
                        for j in range((len(temp[0]))):
                                neighbor= processing[nk]
                                neigh=prevpdb.findneighbor(temp[nk][j],i['res num'])
                                if len(neigh):
                                    if not nk in youmu:
                                        youmu.append(nk)
                                    if not j in countholder:
                                        countholder.append(j)
                    count=-1
                    for eirin in range(len(temp)):
                        count+=1
                        counter=0
                        for yuyuko in countholder:
                            cid='M'
                            if str(temp[eirin][yuyuko][3])!='x,y,z':
                                cid='Z'
                                counter+=1
                            if cid!='M':
                                while len(derp)<counter:
                                    derp.append([])

                                a=updatefinally[count]
                                a.optimum_update(temp[eirin][yuyuko])
                                t0 = "ATOM    957  O   HOH B   1      36.504 -10.582  -2.929  1.00 13.36      A    O"
                                t1 = curres
                                t2 = currpdb
                                tempy = Atom(t0, t1, t2)
                                tempy['x'] = a['x']
                                tempy['y'] = a['y']
                                tempy['z'] = a['z']
                                tempy['res name']=a['res name']
                                tempy['res num']=a['res num']
                                tempy['atom name']=a['atom name']
                                tempy['chain']=cid
                                tempy['atype']=a['atype']
                                tempy['B']=float("%.2d"%count)
                                derp[counter-1].append(tempy)
                                #print tempy
                                #print counter
                                #newpdblines.append(tempy)
                    countholder=[]
        for i in derp:
            for j in i:
                prevpdb.append(j)
                                                     
def run():
    argv = sys.argv[1:]
    try:
        id=argv[0]
    except:
        return

    root =  'Renumbered/'
    if(root[-1:] != '/'):
        root += '/'
    url = 'http://129.10.89.145/running.php?job=%d&status=200'%int(id)
    print url
    raw_return=urllib.urlopen(url).read()
    pdb_filenames = []
    if(argv and 0):
        pdb_filenames = argv
    else:
        filenames = os.listdir(os.getcwd())
        for f in filenames:
            if(f[-4:] == '.pdb'):
                pdb_filenames.append(f)
    a = Analyzer(pdb_filenames, root, 1.0)
    input = ''
    print "Entering Phase"
    a.phase1()
    print "Exiting Phase"
    url = 'http://129.10.89.145/running.php?job=%d&status=300'%int(id)
    raw_return=urllib.urlopen(url).read()
    os.chdir('../Super')
    os.system("python Super.py "+id)
    return
if(__name__ == '__main__'):
    run()
        
        
