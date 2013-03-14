#!/usr/bin/python

#*********************************************************************************
# symgen.py
# Version 1.0
# July 9, 2010 by Bradley M. Kearney
#
#
# This program provides symmetry-realated molecule generation for DRoP.py
#*********************************************************************************


import math
from math import *

from decimal import *
import numpy as N
from numpy.linalg import *
from numpy import *
from pdb import *
import string
import copy

sym_base = {
    (
    'x,y,z',
    ): ['P 1', 'P1'],
    (
    'x,y,z',
    '-x,y,-z',
    ): ['P 1 2 1', 'P 2'],
    (
    'x,y,z',
    '-x,y+1/2,-z',
    ): ['P 1 21 1', 'P 21'],
    (
    'x,y,z',
    '-x,-y,z+1/2',
    ): ['P 1 1 21'],
    (
    'x,y,z',
    '-x,y,-z',
    'x+1/2,y+1/2,z',
    '-x+1/2,y+1/2,-z',
    ): ['C 1 2 1', 'C 2'],
    (
    'x,y,z',
    '-x,-y,z',
    'x,-y,-z',
    '-x,y,-z',
    ): ['P 2 2 2'],
    (
    'x,y,z',
    '-x,-y,z+1/2',
    'x,-y,-z',
    '-x,y,-z+1/2',
    ): ['P 2 2 21'],
    (
    'x,y,z',
    '-x,-y,z',
    'x+1/2,-y+1/2,-z',
    '-x+1/2,y+1/2,-z',
    ): ['P 21 21 2'],
    (
    'x,y,z',
    '-x+1/2,-y,z+1/2',
    'x+1/2,-y+1/2,-z',
    '-x,y+1/2,-z+1/2',
    ): ['P 21 21 21'],
    (
    'x,y,z',
    '-x,-y,z+1/2',
    'x,-y,-z',
    '-x,y,-z+1/2',
    'x+1/2,y+1/2,z',
    '-x+1/2,-y+1/2,z+1/2',
    'x+1/2,-y+1/2,-z',
    '-x+1/2,y+1/2,-z+1/2',
    ): ['C 2 2 21'],
    (
    'x,y,z',
    '-x,-y,z',
    'x,-y,-z',
    '-x,y,-z',
    'x+1/2,y+1/2,z',
    '-x+1/2,-y+1/2,z',
    'x+1/2,-y+1/2,-z',
    '-x+1/2,y+1/2,-z',
    ): ['C 2 2 2'],
    (
    'x,y,z',
    '-x,-y,z',
    'x,-y,-z',
    '-x,y,-z',
    'x,y+1/2,z+1/2',
    '-x,-y+1/2,z+1/2',
    'x,-y+1/2,-z+1/2',
    '-x,y+1/2,-z+1/2',
    'x+1/2,y,z+1/2',
    '-x+1/2,-y,z+1/2',
    'x+1/2,-y,-z+1/2',
    '-x+1/2,y,-z+1/2',
    'x+1/2,y+1/2,z',
    '-x+1/2,-y+1/2,z',
    'x+1/2,-y+1/2,-z',
    '-x+1/2,y+1/2,-z',
    ): ['F 2 2 2'],
    (
    'x,y,z',
    '-x,-y,z',
    'x,-y,-z',
    '-x,y,-z',
    'x+1/2,y+1/2,z+1/2',
    '-x+1/2,-y+1/2,z+1/2',
    'x+1/2,-y+1/2,-z+1/2',
    '-x+1/2,y+1/2,-z+1/2',
    ): ['I 2 2 2'],
    (
    'x,y,z',
    '-x,-y+1/2,z',
    'x,-y,-z+1/2',
    '-x,y+1/2,-z+1/2',
    'x+1/2,y+1/2,z+1/2',
    '-x+1/2,-y,z+1/2',
    'x+1/2,-y+1/2,-z',
    '-x+1/2,y,-z',
    ): ['I 21 21 21'],
    (
    'x,y,z',
    '-y,x,z',
    '-x,-y,z',
    'y,-x,z',
    ): ['P 4'],
    (
    'x,y,z',
    '-y,x,z+1/4',
    '-x,-y,z+1/2',
    'y,-x,z+3/4',
    ): ['P 41'],
    (
    'x,y,z',
    '-y,x,z+1/2',
    '-x,-y,z',
    'y,-x,z+1/2',
    ): ['P 42'],
    (
    'x,y,z',
    '-y,x,z+3/4',
    '-x,-y,z+1/2',
    'y,-x,z+1/4',
    ): ['P 43'],
    (
    'x,y,z',
    '-y,x,z',
    '-x,-y,z',
    'y,-x,z',
    'x+1/2,y+1/2,z+1/2',
    '-y+1/2,x+1/2,z+1/2',
    '-x+1/2,-y+1/2,z+1/2',
    'y+1/2,-x+1/2,z+1/2',
    ): ['I 4'],
    (
    'x,y,z',
    '-y,x+1/2,z+1/4',
    '-x+1/2,-y+1/2,z+1/2',
    'y+1/2,-x,z+3/4',
    'x+1/2,y+1/2,z+1/2',
    '-y+1/2,x,z+3/4',
    '-x,-y,z',
    'y,-x+1/2,z+1/4',
    ): ['I 41'],
    (
    'x,y,z',
    '-y,x,z',
    '-x,-y,z',
    'y,-x,z',
    'x,-y,-z',
    'y,x,-z',
    '-x,y,-z',
    '-y,-x,-z',
    ): ['P 4 2 2'],
    (
    'x,y,z',
    '-y+1/2,x+1/2,z',
    '-x,-y,z',
    'y+1/2,-x+1/2,z',
    'x+1/2,-y+1/2,-z',
    'y,x,-z',
    '-x+1/2,y+1/2,-z',
    '-y,-x,-z',
    ): ['P 4 21 2'],
    (
    'x,y,z',
    '-y,x,z+1/4',
    '-x,-y,z+1/2',
    'y,-x,z+3/4',
    'x,-y,-z+1/2',
    'y,x,-z+3/4',
    '-x,y,-z',
    '-y,-x,-z+1/4',
    ): ['P 41 2 2'],
    (
    'x,y,z',
    '-y+1/2,x+1/2,z+1/4',
    '-x,-y,z+1/2',
    'y+1/2,-x+1/2,z+3/4',
    'x+1/2,-y+1/2,-z+3/4',
    'y,x,-z',
    '-x+1/2,y+1/2,-z+1/4',
    '-y,-x,-z+1/2',
    ): ['P 41 21 2'],
    (
    'x,y,z',
    '-y,x,z+1/2',
    '-x,-y,z',
    'y,-x,z+1/2',
    'x,-y,-z',
    'y,x,-z+1/2',
    '-x,y,-z',
    '-y,-x,-z+1/2',
    ): ['P 42 2 2'],
    (
    'x,y,z',
    '-y+1/2,x+1/2,z+1/2',
    '-x,-y,z',
    'y+1/2,-x+1/2,z+1/2',
    'x+1/2,-y+1/2,-z+1/2',
    'y,x,-z',
    '-x+1/2,y+1/2,-z+1/2',
    '-y,-x,-z',
    ): ['P 42 21 2'],
    (
    'x,y,z',
    '-y,x,z+3/4',
    '-x,-y,z+1/2',
    'y,-x,z+1/4',
    'x,-y,-z+1/2',
    'y,x,-z+1/4',
    '-x,y,-z',
    '-y,-x,-z+3/4',
    ): ['P 43 2 2'],
    (
    'x,y,z',
    '-y+1/2,x+1/2,z+3/4',
    '-x,-y,z+1/2',
    'y+1/2,-x+1/2,z+1/4',
    'x+1/2,-y+1/2,-z+1/4',
    'y,x,-z',
    '-x+1/2,y+1/2,-z+3/4',
    '-y,-x,-z+1/2',
    ): ['P 43 21 2'],
    (
    'x,y,z',
    '-y,x,z',
    '-x,-y,z',
    'y,-x,z',
    'x,-y,-z',
    'y,x,-z',
    '-x,y,-z',
    '-y,-x,-z',
    'x+1/2,y+1/2,z+1/2',
    '-y+1/2,x+1/2,z+1/2',
    '-x+1/2,-y+1/2,z+1/2',
    'y+1/2,-x+1/2,z+1/2',
    'x+1/2,-y+1/2,-z+1/2',
    'y+1/2,x+1/2,-z+1/2',
    '-x+1/2,y+1/2,-z+1/2',
    '-y+1/2,-x+1/2,-z+1/2',
    ): ['I 4 2 2'],
    (
    'x,y,z',
    '-y,x+1/2,z+1/4',
    '-x+1/2,-y+1/2,z+1/2',
    'y+1/2,-x,z+3/4',
    'x,-y+1/2,-z+1/4',
    'y+1/2,x+1/2,-z+1/2',
    '-x+1/2,y,-z+3/4',
    '-y,-x,-z',
    'x+1/2,y+1/2,z+1/2',
    '-y+1/2,x,z+3/4',
    '-x,-y,z',
    'y,-x+1/2,z+1/4',
    'x+1/2,-y,-z+3/4',
    'y,x,-z',
    '-x,y+1/2,-z+1/4',
    '-y+1/2,-x+1/2,-z+1/2',
    ): ['I 41 2 2'],
    (
    'x,y,z',
    '-y,x-y,z',
    '-x+y,-x,z',
    ): ['P 3'],
    (
    'x,y,z',
    '-y,x-y,z+1/3',
    '-x+y,-x,z+2/3',
    ): ['P 31'],
    (
    'x,y,z',
    '-y,x-y,z+2/3',
    '-x+y,-x,z+1/3',
    ): ['P 32'],
    (
    'x,y,z',
    '-y,x-y,z',
    '-x+y,-x,z',
    'x+2/3,y+1/3,z+1/3',
    '-y+2/3,x-y+1/3,z+1/3',
    '-x+y+2/3,-x+1/3,z+1/3',
    'x+1/3,y+2/3,z+2/3',
    '-y+1/3,x-y+2/3,z+2/3',
    '-x+y+1/3,-x+2/3,z+2/3',
    ): ['H 3', 'R 3', 'R 3 :H', 'R 3:H'],
    (
    'x,y,z',
    '-y,x-y,z',
    '-x+y,-x,z',
    '-y,-x,-z',
    'x,x-y,-z',
    '-x+y,y,-z',
    ): ['P 3 1 2'],
    (
    'x,y,z',
    '-y,x-y,z',
    '-x+y,-x,z',
    'y,x,-z',
    '-x,-x+y,-z',
    'x-y,-y,-z',
    ): ['P 3 2 1'],
    (
    'x,y,z',
    '-y,x-y,z+1/3',
    '-x+y,-x,z+2/3',
    '-y,-x,-z+2/3',
    'x,x-y,-z',
    '-x+y,y,-z+1/3',
    ): ['P 31 1 2'],
    (
    'x,y,z',
    '-y,x-y,z+1/3',
    '-x+y,-x,z+2/3',
    'y,x,-z',
    '-x,-x+y,-z+1/3',
    'x-y,-y,-z+2/3',
    ): ['P 31 2 1'],
    (
    'x,y,z',
    '-y,x-y,z+2/3',
    '-x+y,-x,z+1/3',
    '-y,-x,-z+1/3',
    'x,x-y,-z',
    '-x+y,y,-z+2/3',
    ): ['P 32 1 2'],
    (
    'x,y,z',
    '-y,x-y,z+2/3',
    '-x+y,-x,z+1/3',
    'y,x,-z',
    '-x,-x+y,-z+2/3',
    'x-y,-y,-z+1/3',
    ): ['P 32 2 1'],
    (
    'x,y,z',
    '-y,x-y,z',
    '-x+y,-x,z',
    'y,x,-z',
    '-x,-x+y,-z',
    'x-y,-y,-z',
    'x+2/3,y+1/3,z+1/3',
    '-y+2/3,x-y+1/3,z+1/3',
    '-x+y+2/3,-x+1/3,z+1/3',
    'y+2/3,x+1/3,-z+1/3',
    '-x+2/3,-x+y+1/3,-z+1/3',
    'x-y+2/3,-y+1/3,-z+1/3',
    'x+1/3,y+2/3,z+2/3',
    '-y+1/3,x-y+2/3,z+2/3',
    '-x+y+1/3,-x+2/3,z+2/3',
    'y+1/3,x+2/3,-z+2/3',
    '-x+1/3,-x+y+2/3,-z+2/3',
    'x-y+1/3,-y+2/3,-z+2/3',
    ): ['H 3 2', 'R 3 2', 'R 3 2 :H', 'R 3 2:H', 'R 32'],
    (
    'x,y,z',
    'x-y,x,z',
    '-y,x-y,z',
    '-x,-y,z',
    '-x+y,-x,z',
    'y,-x+y,z',
    ): ['P 6'],
    (
    'x,y,z',
    'x-y,x,z+1/6',
    '-y,x-y,z+1/3',
    '-x,-y,z+1/2',
    '-x+y,-x,z+2/3',
    'y,-x+y,z+5/6',
    ): ['P 61'],
    (
    'x,y,z',
    'x-y,x,z+5/6',
    '-y,x-y,z+2/3',
    '-x,-y,z+1/2',
    '-x+y,-x,z+1/3',
    'y,-x+y,z+1/6',
    ): ['P 65'],
    (
    'x,y,z',
    'x-y,x,z+1/3',
    '-y,x-y,z+2/3',
    '-x,-y,z',
    '-x+y,-x,z+1/3',
    'y,-x+y,z+2/3',
    ): ['P 62'],
    (
    'x,y,z',
    'x-y,x,z+2/3',
    '-y,x-y,z+1/3',
    '-x,-y,z',
    '-x+y,-x,z+2/3',
    'y,-x+y,z+1/3',
    ): ['P 64'],
    (
    'x,y,z',
    'x-y,x,z+1/2',
    '-y,x-y,z',
    '-x,-y,z+1/2',
    '-x+y,-x,z',
    'y,-x+y,z+1/2',
    ): ['P 63'],
    (
    'x,y,z',
    'x-y,x,z',
    '-y,x-y,z',
    '-x,-y,z',
    '-x+y,-x,z',
    'y,-x+y,z',
    '-y,-x,-z',
    'x-y,-y,-z',
    'x,x-y,-z',
    'y,x,-z',
    '-x+y,y,-z',
    '-x,-x+y,-z',
    ): ['P 6 2 2'],
    (
    'x,y,z',
    'x-y,x,z+1/6',
    '-y,x-y,z+1/3',
    '-x,-y,z+1/2',
    '-x+y,-x,z+2/3',
    'y,-x+y,z+5/6',
    '-y,-x,-z+5/6',
    'x-y,-y,-z',
    'x,x-y,-z+1/6',
    'y,x,-z+1/3',
    '-x+y,y,-z+1/2',
    '-x,-x+y,-z+2/3',
    ): ['P 61 2 2'],
    (
    'x,y,z',
    'x-y,x,z+1/3',
    '-y,x-y,z+2/3',
    '-x,-y,z',
    '-x+y,-x,z+1/3',
    'y,-x+y,z+2/3',
    '-y,-x,-z+2/3',
    'x-y,-y,-z',
    'x,x-y,-z+1/3',
    'y,x,-z+2/3',
    '-x+y,y,-z',
    '-x,-x+y,-z+1/3',
    ): ['P 62 2 2'],
    (
    'x,y,z',
    'x-y,x,z+2/3',
    '-y,x-y,z+1/3',
    '-x,-y,z',
    '-x+y,-x,z+2/3',
    'y,-x+y,z+1/3',
    '-y,-x,-z+1/3',
    'x-y,-y,-z',
    'x,x-y,-z+2/3',
    'y,x,-z+1/3',
    '-x+y,y,-z',
    '-x,-x+y,-z+2/3',
    ): ['P 64 2 2'],
    (
    'x,y,z',
    'x-y,x,z+5/6',
    '-y,x-y,z+2/3',
    '-x,-y,z+1/2',
    '-x+y,-x,z+1/3',
    'y,-x+y,z+1/6',
    '-y,-x,-z+1/6',
    'x-y,-y,-z',
    'x,x-y,-z+5/6',
    'y,x,-z+2/3',
    '-x+y,y,-z+1/2',
    '-x,-x+y,-z+1/3',
    ): ['P 65 2 2'],
    (
    'x,y,z',
    'x-y,x,z+1/2',
    '-y,x-y,z',
    '-x,-y,z+1/2',
    '-x+y,-x,z',
    'y,-x+y,z+1/2',
    '-y,-x,-z+1/2',
    'x-y,-y,-z',
    'x,x-y,-z+1/2',
    'y,x,-z',
    '-x+y,y,-z+1/2',
    '-x,-x+y,-z',
    ): ['P 63 2 2'],
    (
    'x,y,z',
    '-x,-y,z',
    'x,-y,-z',
    '-x,y,-z',
    'z,x,y',
    '-z,-x,y',
    'z,-x,-y',
    '-z,x,-y',
    'y,z,x',
    'y,-z,-x',
    '-y,z,-x',
    '-y,-z,x',
    ): ['P 2 3'],
    (
    'x,y,z',
    '-x,-y,z',
    'x,-y,-z',
    '-x,y,-z',
    'z,x,y',
    '-z,-x,y',
    'z,-x,-y',
    '-z,x,-y',
    'y,z,x',
    'y,-z,-x',
    '-y,z,-x',
    '-y,-z,x',
    'x,y+1/2,z+1/2',
    '-x,-y+1/2,z+1/2',
    'x,-y+1/2,-z+1/2',
    '-x,y+1/2,-z+1/2',
    'z,x+1/2,y+1/2',
    '-z,-x+1/2,y+1/2',
    'z,-x+1/2,-y+1/2',
    '-z,x+1/2,-y+1/2',
    'y,z+1/2,x+1/2',
    'y,-z+1/2,-x+1/2',
    '-y,z+1/2,-x+1/2',
    '-y,-z+1/2,x+1/2',
    'x+1/2,y,z+1/2',
    '-x+1/2,-y,z+1/2',
    'x+1/2,-y,-z+1/2',
    '-x+1/2,y,-z+1/2',
    'z+1/2,x,y+1/2',
    '-z+1/2,-x,y+1/2',
    'z+1/2,-x,-y+1/2',
    '-z+1/2,x,-y+1/2',
    'y+1/2,z,x+1/2',
    'y+1/2,-z,-x+1/2',
    '-y+1/2,z,-x+1/2',
    '-y+1/2,-z,x+1/2',
    'x+1/2,y+1/2,z',
    '-x+1/2,-y+1/2,z',
    'x+1/2,-y+1/2,-z',
    '-x+1/2,y+1/2,-z',
    'z+1/2,x+1/2,y',
    '-z+1/2,-x+1/2,y',
    'z+1/2,-x+1/2,-y',
    '-z+1/2,x+1/2,-y',
    'y+1/2,z+1/2,x',
    'y+1/2,-z+1/2,-x',
    '-y+1/2,z+1/2,-x',
    '-y+1/2,-z+1/2,x',
    ): ['F 2 3'],
    (
    'x,y,z',
    '-x,-y,z',
    'x,-y,-z',
    '-x,y,-z',
    'z,x,y',
    '-z,-x,y',
    'z,-x,-y',
    '-z,x,-y',
    'y,z,x',
    'y,-z,-x',
    '-y,z,-x',
    '-y,-z,x',
    'x+1/2,y+1/2,z+1/2',
    '-x+1/2,-y+1/2,z+1/2',
    'x+1/2,-y+1/2,-z+1/2',
    '-x+1/2,y+1/2,-z+1/2',
    'z+1/2,x+1/2,y+1/2',
    '-z+1/2,-x+1/2,y+1/2',
    'z+1/2,-x+1/2,-y+1/2',
    '-z+1/2,x+1/2,-y+1/2',
    'y+1/2,z+1/2,x+1/2',
    'y+1/2,-z+1/2,-x+1/2',
    '-y+1/2,z+1/2,-x+1/2',
    '-y+1/2,-z+1/2,x+1/2',
    ): ['I 2 3', 'I 23'],
    (
    'x,y,z',
    '-x+1/2,-y,z+1/2',
    'x+1/2,-y+1/2,-z',
    '-x,y+1/2,-z+1/2',
    'z,x,y',
    '-z+1/2,-x,y+1/2',
    'z+1/2,-x+1/2,-y',
    '-z,x+1/2,-y+1/2',
    'y,z,x',
    'y+1/2,-z+1/2,-x',
    '-y,z+1/2,-x+1/2',
    '-y+1/2,-z,x+1/2',
    ): ['P 21 3'],
    (
    'x,y,z',
    '-x,-y+1/2,z',
    'x,-y,-z+1/2',
    '-x,y+1/2,-z+1/2',
    'z,x,y',
    '-z,-x+1/2,y',
    'z,-x,-y+1/2',
    '-z,x+1/2,-y+1/2',
    'y,z,x',
    'y,-z,-x+1/2',
    '-y,z+1/2,-x+1/2',
    '-y+1/2,-z,x+1/2',
    'x+1/2,y+1/2,z+1/2',
    '-x+1/2,-y,z+1/2',
    'x+1/2,-y+1/2,-z',
    '-x+1/2,y,-z',
    'z+1/2,x+1/2,y+1/2',
    '-z+1/2,-x,y+1/2',
    'z+1/2,-x+1/2,-y',
    '-z+1/2,x,-y',
    'y+1/2,z+1/2,x+1/2',
    'y+1/2,-z+1/2,-x',
    '-y+1/2,z,-x',
    '-y,-z+1/2,x',
    ): ['I 21 3'],
    (
    'x,y,z',
    '-y,x,z',
    '-x,-y,z',
    'y,-x,z',
    'x,-y,-z',
    'y,x,-z',
    '-x,y,-z',
    '-y,-x,-z',
    'z,x,y',
    '-x,z,y',
    '-z,-x,y',
    'x,-z,y',
    'z,-x,-y',
    'x,z,-y',
    '-z,x,-y',
    '-x,-z,-y',
    'y,z,x',
    'y,-z,-x',
    'z,y,-x',
    '-y,z,-x',
    '-z,-y,-x',
    '-y,-z,x',
    'z,-y,x',
    '-z,y,x',
    ): ['P 4 3 2'],
    (
    'x,y,z',
    '-y+1/2,x+1/2,z+1/2',
    '-x,-y,z',
    'y+1/2,-x+1/2,z+1/2',
    'x,-y,-z',
    'y+1/2,x+1/2,-z+1/2',
    '-x,y,-z',
    '-y+1/2,-x+1/2,-z+1/2',
    'z,x,y',
    '-x+1/2,z+1/2,y+1/2',
    '-z,-x,y',
    'x+1/2,-z+1/2,y+1/2',
    'z,-x,-y',
    'x+1/2,z+1/2,-y+1/2',
    '-z,x,-y',
    '-x+1/2,-z+1/2,-y+1/2',
    'y,z,x',
    'y,-z,-x',
    'z+1/2,y+1/2,-x+1/2',
    '-y,z,-x',
    '-z+1/2,-y+1/2,-x+1/2',
    '-y,-z,x',
    'z+1/2,-y+1/2,x+1/2',
    '-z+1/2,y+1/2,x+1/2',
    ): ['P 42 3 2'],
    (
    'x,y,z',
    '-y,x,z',
    '-x,-y,z',
    'y,-x,z',
    'x,-y,-z',
    'y,x,-z',
    '-x,y,-z',
    '-y,-x,-z',
    'z,x,y',
    '-x,z,y',
    '-z,-x,y',
    'x,-z,y',
    'z,-x,-y',
    'x,z,-y',
    '-z,x,-y',
    '-x,-z,-y',
    'y,z,x',
    'y,-z,-x',
    'z,y,-x',
    '-y,z,-x',
    '-z,-y,-x',
    '-y,-z,x',
    'z,-y,x',
    '-z,y,x',
    'x,y+1/2,z+1/2',
    '-y,x+1/2,z+1/2',
    '-x,-y+1/2,z+1/2',
    'y,-x+1/2,z+1/2',
    'x,-y+1/2,-z+1/2',
    'y,x+1/2,-z+1/2',
    '-x,y+1/2,-z+1/2',
    '-y,-x+1/2,-z+1/2',
    'z,x+1/2,y+1/2',
    '-x,z+1/2,y+1/2',
    '-z,-x+1/2,y+1/2',
    'x,-z+1/2,y+1/2',
    'z,-x+1/2,-y+1/2',
    'x,z+1/2,-y+1/2',
    '-z,x+1/2,-y+1/2',
    '-x,-z+1/2,-y+1/2',
    'y,z+1/2,x+1/2',
    'y,-z+1/2,-x+1/2',
    'z,y+1/2,-x+1/2',
    '-y,z+1/2,-x+1/2',
    '-z,-y+1/2,-x+1/2',
    '-y,-z+1/2,x+1/2',
    'z,-y+1/2,x+1/2',
    '-z,y+1/2,x+1/2',
    'x+1/2,y,z+1/2',
    '-y+1/2,x,z+1/2',
    '-x+1/2,-y,z+1/2',
    'y+1/2,-x,z+1/2',
    'x+1/2,-y,-z+1/2',
    'y+1/2,x,-z+1/2',
    '-x+1/2,y,-z+1/2',
    '-y+1/2,-x,-z+1/2',
    'z+1/2,x,y+1/2',
    '-x+1/2,z,y+1/2',
    '-z+1/2,-x,y+1/2',
    'x+1/2,-z,y+1/2',
    'z+1/2,-x,-y+1/2',
    'x+1/2,z,-y+1/2',
    '-z+1/2,x,-y+1/2',
    '-x+1/2,-z,-y+1/2',
    'y+1/2,z,x+1/2',
    'y+1/2,-z,-x+1/2',
    'z+1/2,y,-x+1/2',
    '-y+1/2,z,-x+1/2',
    '-z+1/2,-y,-x+1/2',
    '-y+1/2,-z,x+1/2',
    'z+1/2,-y,x+1/2',
    '-z+1/2,y,x+1/2',
    'x+1/2,y+1/2,z',
    '-y+1/2,x+1/2,z',
    '-x+1/2,-y+1/2,z',
    'y+1/2,-x+1/2,z',
    'x+1/2,-y+1/2,-z',
    'y+1/2,x+1/2,-z',
    '-x+1/2,y+1/2,-z',
    '-y+1/2,-x+1/2,-z',
    'z+1/2,x+1/2,y',
    '-x+1/2,z+1/2,y',
    '-z+1/2,-x+1/2,y',
    'x+1/2,-z+1/2,y',
    'z+1/2,-x+1/2,-y',
    'x+1/2,z+1/2,-y',
    '-z+1/2,x+1/2,-y',
    '-x+1/2,-z+1/2,-y',
    'y+1/2,z+1/2,x',
    'y+1/2,-z+1/2,-x',
    'z+1/2,y+1/2,-x',
    '-y+1/2,z+1/2,-x',
    '-z+1/2,-y+1/2,-x',
    '-y+1/2,-z+1/2,x',
    'z+1/2,-y+1/2,x',
    '-z+1/2,y+1/2,x',
    ): ['F 4 3 2'],
    (
    'x,y,z',
    '-y+1/4,x+1/4,z+1/4',
    '-x,-y+1/2,z+1/2',
    'y+3/4,-x+1/4,z+3/4',
    'x,-y,-z',
    'y+1/4,x+1/4,-z+1/4',
    '-x,y+1/2,-z+1/2',
    '-y+3/4,-x+1/4,-z+3/4',
    'z,x,y',
    '-x+1/4,z+1/4,y+1/4',
    '-z,-x+1/2,y+1/2',
    'x+3/4,-z+1/4,y+3/4',
    'z,-x,-y',
    'x+1/4,z+1/4,-y+1/4',
    '-z,x+1/2,-y+1/2',
    '-x+3/4,-z+1/4,-y+3/4',
    'y,z,x',
    'y+1/2,-z,-x+1/2',
    'z+1/4,y+3/4,-x+3/4',
    '-y+1/2,z+1/2,-x',
    '-z+1/4,-y+1/4,-x+1/4',
    '-y,-z,x',
    'z+1/4,-y+3/4,x+3/4',
    '-z+3/4,y+3/4,x+1/4',
    'x,y+1/2,z+1/2',
    '-y+1/4,x+3/4,z+3/4',
    '-x,-y,z',
    'y+3/4,-x+3/4,z+1/4',
    'x,-y+1/2,-z+1/2',
    'y+1/4,x+3/4,-z+3/4',
    '-x,y,-z',
    '-y+3/4,-x+3/4,-z+1/4',
    'z,x+1/2,y+1/2',
    '-x+1/4,z+3/4,y+3/4',
    '-z,-x,y',
    'x+3/4,-z+3/4,y+1/4',
    'z,-x+1/2,-y+1/2',
    'x+1/4,z+3/4,-y+3/4',
    '-z,x,-y',
    '-x+3/4,-z+3/4,-y+1/4',
    'y,z+1/2,x+1/2',
    'y+1/2,-z+1/2,-x',
    'z+1/4,y+1/4,-x+1/4',
    '-y+1/2,z,-x+1/2',
    '-z+1/4,-y+3/4,-x+3/4',
    '-y,-z+1/2,x+1/2',
    'z+1/4,-y+1/4,x+1/4',
    '-z+3/4,y+1/4,x+3/4',
    'x+1/2,y,z+1/2',
    '-y+3/4,x+1/4,z+3/4',
    '-x+1/2,-y+1/2,z',
    'y+1/4,-x+1/4,z+1/4',
    'x+1/2,-y,-z+1/2',
    'y+3/4,x+1/4,-z+3/4',
    '-x+1/2,y+1/2,-z',
    '-y+1/4,-x+1/4,-z+1/4',
    'z+1/2,x,y+1/2',
    '-x+3/4,z+1/4,y+3/4',
    '-z+1/2,-x+1/2,y',
    'x+1/4,-z+1/4,y+1/4',
    'z+1/2,-x,-y+1/2',
    'x+3/4,z+1/4,-y+3/4',
    '-z+1/2,x+1/2,-y',
    '-x+1/4,-z+1/4,-y+1/4',
    'y+1/2,z,x+1/2',
    'y,-z,-x',
    'z+3/4,y+3/4,-x+1/4',
    '-y,z+1/2,-x+1/2',
    '-z+3/4,-y+1/4,-x+3/4',
    '-y+1/2,-z,x+1/2',
    'z+3/4,-y+3/4,x+1/4',
    '-z+1/4,y+3/4,x+3/4',
    'x+1/2,y+1/2,z',
    '-y+3/4,x+3/4,z+1/4',
    '-x+1/2,-y,z+1/2',
    'y+1/4,-x+3/4,z+3/4',
    'x+1/2,-y+1/2,-z',
    'y+3/4,x+3/4,-z+1/4',
    '-x+1/2,y,-z+1/2',
    '-y+1/4,-x+3/4,-z+3/4',
    'z+1/2,x+1/2,y',
    '-x+3/4,z+3/4,y+1/4',
    '-z+1/2,-x,y+1/2',
    'x+1/4,-z+3/4,y+3/4',
    'z+1/2,-x+1/2,-y',
    'x+3/4,z+3/4,-y+1/4',
    '-z+1/2,x,-y+1/2',
    '-x+1/4,-z+3/4,-y+3/4',
    'y+1/2,z+1/2,x',
    'y,-z+1/2,-x+1/2',
    'z+3/4,y+1/4,-x+3/4',
    '-y,z,-x',
    '-z+3/4,-y+3/4,-x+1/4',
    '-y+1/2,-z+1/2,x',
    'z+3/4,-y+1/4,x+3/4',
    '-z+1/4,y+1/4,x+1/4',
    ): ['F 41 3 2'],
    (
    'x,y,z',
    '-y,x,z',
    '-x,-y,z',
    'y,-x,z',
    'x,-y,-z',
    'y,x,-z',
    '-x,y,-z',
    '-y,-x,-z',
    'z,x,y',
    '-x,z,y',
    '-z,-x,y',
    'x,-z,y',
    'z,-x,-y',
    'x,z,-y',
    '-z,x,-y',
    '-x,-z,-y',
    'y,z,x',
    'y,-z,-x',
    'z,y,-x',
    '-y,z,-x',
    '-z,-y,-x',
    '-y,-z,x',
    'z,-y,x',
    '-z,y,x',
    'x+1/2,y+1/2,z+1/2',
    '-y+1/2,x+1/2,z+1/2',
    '-x+1/2,-y+1/2,z+1/2',
    'y+1/2,-x+1/2,z+1/2',
    'x+1/2,-y+1/2,-z+1/2',
    'y+1/2,x+1/2,-z+1/2',
    '-x+1/2,y+1/2,-z+1/2',
    '-y+1/2,-x+1/2,-z+1/2',
    'z+1/2,x+1/2,y+1/2',
    '-x+1/2,z+1/2,y+1/2',
    '-z+1/2,-x+1/2,y+1/2',
    'x+1/2,-z+1/2,y+1/2',
    'z+1/2,-x+1/2,-y+1/2',
    'x+1/2,z+1/2,-y+1/2',
    '-z+1/2,x+1/2,-y+1/2',
    '-x+1/2,-z+1/2,-y+1/2',
    'y+1/2,z+1/2,x+1/2',
    'y+1/2,-z+1/2,-x+1/2',
    'z+1/2,y+1/2,-x+1/2',
    '-y+1/2,z+1/2,-x+1/2',
    '-z+1/2,-y+1/2,-x+1/2',
    '-y+1/2,-z+1/2,x+1/2',
    'z+1/2,-y+1/2,x+1/2',
    '-z+1/2,y+1/2,x+1/2',
    ): ['I 4 3 2'],
    (
    'x,y,z',
    '-y+3/4,x+1/4,z+3/4',
    '-x+1/2,-y,z+1/2',
    'y+3/4,-x+3/4,z+1/4',
    'x+1/2,-y+1/2,-z',
    'y+1/4,x+3/4,-z+3/4',
    '-x,y+1/2,-z+1/2',
    '-y+1/4,-x+1/4,-z+1/4',
    'z,x,y',
    '-x+3/4,z+1/4,y+3/4',
    '-z+1/2,-x,y+1/2',
    'x+3/4,-z+3/4,y+1/4',
    'z+1/2,-x+1/2,-y',
    'x+1/4,z+3/4,-y+3/4',
    '-z,x+1/2,-y+1/2',
    '-x+1/4,-z+1/4,-y+1/4',
    'y,z,x',
    'y+1/2,-z+1/2,-x',
    'z+1/4,y+3/4,-x+3/4',
    '-y,z+1/2,-x+1/2',
    '-z+1/4,-y+1/4,-x+1/4',
    '-y+1/2,-z,x+1/2',
    'z+3/4,-y+3/4,x+1/4',
    '-z+3/4,y+1/4,x+3/4',
    ): ['P 43 3 2'],
    (
    'x,y,z',
    '-y+1/4,x+3/4,z+1/4',
    '-x+1/2,-y,z+1/2',
    'y+1/4,-x+1/4,z+3/4',
    'x+1/2,-y+1/2,-z',
    'y+3/4,x+1/4,-z+1/4',
    '-x,y+1/2,-z+1/2',
    '-y+3/4,-x+3/4,-z+3/4',
    'z,x,y',
    '-x+1/4,z+3/4,y+1/4',
    '-z+1/2,-x,y+1/2',
    'x+1/4,-z+1/4,y+3/4',
    'z+1/2,-x+1/2,-y',
    'x+3/4,z+1/4,-y+1/4',
    '-z,x+1/2,-y+1/2',
    '-x+3/4,-z+3/4,-y+3/4',
    'y,z,x',
    'y+1/2,-z+1/2,-x',
    'z+3/4,y+1/4,-x+1/4',
    '-y,z+1/2,-x+1/2',
    '-z+3/4,-y+3/4,-x+3/4',
    '-y+1/2,-z,x+1/2',
    'z+1/4,-y+1/4,x+3/4',
    '-z+1/4,y+3/4,x+1/4',
    ): ['P 41 3 2'],
    (
    'x,y,z',
    '-y+1/4,x+3/4,z+1/4',
    '-x+1/2,-y,z+1/2',
    'y+1/4,-x+1/4,z+3/4',
    'x,-y,-z+1/2',
    'y+1/4,x+3/4,-z+3/4',
    '-x+1/2,y,-z',
    '-y+1/4,-x+1/4,-z+1/4',
    'z,x,y',
    '-x+1/4,z+3/4,y+1/4',
    '-z+1/2,-x,y+1/2',
    'x+1/4,-z+1/4,y+3/4',
    'z,-x,-y+1/2',
    'x+1/4,z+3/4,-y+3/4',
    '-z+1/2,x,-y',
    '-x+1/4,-z+1/4,-y+1/4',
    'y,z,x',
    'y+1/2,-z+1/2,-x',
    'z+3/4,y+1/4,-x+1/4',
    '-y,z+1/2,-x+1/2',
    '-z+1/4,-y+1/4,-x+1/4',
    '-y+1/2,-z,x+1/2',
    'z+3/4,-y+3/4,x+1/4',
    '-z+3/4,y+1/4,x+3/4',
    'x+1/2,y+1/2,z+1/2',
    '-y+3/4,x+1/4,z+3/4',
    '-x,-y+1/2,z',
    'y+3/4,-x+3/4,z+1/4',
    'x+1/2,-y+1/2,-z',
    'y+3/4,x+1/4,-z+1/4',
    '-x,y+1/2,-z+1/2',
    '-y+3/4,-x+3/4,-z+3/4',
    'z+1/2,x+1/2,y+1/2',
    '-x+3/4,z+1/4,y+3/4',
    '-z,-x+1/2,y',
    'x+3/4,-z+3/4,y+1/4',
    'z+1/2,-x+1/2,-y',
    'x+3/4,z+1/4,-y+1/4',
    '-z,x+1/2,-y+1/2',
    '-x+3/4,-z+3/4,-y+3/4',
    'y+1/2,z+1/2,x+1/2',
    'y,-z,-x+1/2',
    'z+1/4,y+3/4,-x+3/4',
    '-y+1/2,z,-x',
    '-z+3/4,-y+3/4,-x+3/4',
    '-y,-z+1/2,x',
    'z+1/4,-y+1/4,x+3/4',
    '-z+1/4,y+3/4,x+1/4',
    ): ['I 41 3 2'],    
}

space_groups = {}
for key in sym_base.keys():
    for sym in sym_base[key]:
        space_groups[sym] = key
        
def generate_coordinates3(x, m, t, z):
    new=[]
    new.append(m[0]*(x[0]+m[12]) + m[1]*(x[1]+m[13]) +  m[2]*(x[2]+m[14]) + m[3])
    new.append(m[4]*(x[0]+m[12]) + m[5]*(x[1]+m[13]) +  m[6]*(x[2]+m[14]) + m[7]) 
    new.append(m[8]*(x[0]+m[12]) + m[9]*(x[1]+m[13]) + m[10]*(x[2]+m[14]) + m[11])
    new.append(t)
    new.append(z)
    return new

def generate_coordinates(oper, orig, UC, operstr):
    mycoord = []
    myscrews = []
    ocoord = matrix([orig[0], orig[1], orig[2]])
    fract = ocoord * orig[4]
    fract[0, 0] = fract[0, 0] + 1 * UC[0]
    fract[0, 1] = fract[0, 1] + 1 * UC[1]
    fract[0, 2] = fract[0, 2] + 1 * UC[2]
    oscrew = ocoord
    for i in range(0, len(oper)):
        nx = round(fract[0, 0] * (oper[i][0]), 3)
        ny = round(fract[0, 1] * (oper[i][1]), 3)
        nz = round(fract[0, 2] * (oper[i][2]), 3)
        nd = oper[i][3]
        mycoord.append(nx + ny + nz + nd)
    rcoord = mycoord * orig[3]#return coord
    count = 0
    return [rcoord[0, 0], rcoord[0, 1], rcoord[0, 2], operstr, UC]

def generate_coordinates2(oper, orig, UC):
    mycoord = []
    myscrews = []
    ocoord = matrix([orig[0], orig[1], orig[2]])
    fract = ocoord * orig[4]
    fract[0, 0] = fract[0, 0] + 1 * UC[0]
    fract[0, 1] = fract[0, 1] + 1 * UC[1]
    fract[0, 2] = fract[0, 2] + 1 * UC[2]
    oscrew = ocoord
    for i in range(0, len(oper)):
        nx = round(fract[0, 0] * (oper[i][0]), 3)
        ny = round(fract[0, 1] * (oper[i][1]), 3)
        nz = round(fract[0, 2] * (oper[i][2]), 3)
        nd = oper[i][3]
        mycoord.append(nx + ny + nz + nd)

    rcoord = mycoord * orig[3]#return coord
    count = 0
    return [rcoord[0, 0], rcoord[0, 1], rcoord[0, 2]]
expr_to_vect = {    
    'x-y': [1.0,-1.0,0.0,0.0],
    'x-y+1/3': [1.0,-1.0,0.0,1.0/3.0],
    'x-y+2/3': [1.0,-1.0,0.0,2.0/3.0],
    'x': [1.0,0.0,0.0,0.0],
    'x+1/4': [1.0,0.0,0.0,1.0/4.0],
    'x+1/3': [1.0,0.0,0.0,1.0/3.0],
    'x+1/2': [1.0,0.0,0.0,1.0/2.0],
    'x+2/3': [1.0,0.0,0.0,2.0/3.0],
    'x+3/4': [1.0,0.0,0.0,3.0/4.0],
    '-x+y': [-1.0,1.0,0.0,0.0],
    '-x+y+1/3': [-1.0,1.0,0.0,1.0/3.0],
    '-x+y+2/3': [-1.0,1.0,0.0,2.0/3.0],
    '-x': [-1.0,0.0,0.0,0.0],
    '-x+1/4': [-1.0,0.0,0.0,1.0/4.0],
    '-x+1/3': [-1.0,0.0,0.0,1.0/3.0],
    '-x+1/2': [-1.0,0.0,0.0,1.0/2.0],
    '-x+2/3': [-1.0,0.0,0.0,2.0/3.0],
    '-x+3/4': [-1.0,0.0,0.0,3.0/4.0],
    'y': [0.0,1.0,0.0,0.0],
    'y+1/4': [0.0,1.0,0.0,1.0/4.0],
    'y+1/3': [0.0,1.0,0.0,1.0/3.0],
    'y+1/2': [0.0,1.0,0.0,1.0/2.0],
    'y+2/3': [0.0,1.0,0.0,2.0/3.0],
    'y+3/4': [0.0,1.0,0.0,3.0/4.0],
    '-y': [0.0,-1.0,0.0,0.0],
    '-y+1/4': [0.0,-1.0,0.0,1.0/4.0],
    '-y+1/3': [0.0,-1.0,0.0,1.0/3.0],
    '-y+1/2': [0.0,-1.0,0.0,1.0/2.0],
    '-y+2/3': [0.0,-1.0,0.0,2.0/3.0],
    '-y+3/4': [0.0,-1.0,0.0,3.0/4.0],
    'z': [0.0,0.0,1.0,0.0],
    'z+1/6': [0.0,0.0,1.0,1.0/6.0],
    'z+1/4': [0.0,0.0,1.0,1.0/4.0],
    'z+1/3': [0.0,0.0,1.0,1.0/3.0],
    'z+1/2': [0.0,0.0,1.0,1.0/2.0],
    'z+2/3': [0.0,0.0,1.0,2.0/3.0],
    'z+3/4': [0.0,0.0,1.0,3.0/4.0],
    'z+5/6': [0.0,0.0,1.0,5.0/6.0],
    '-z': [0.0,0.0,-1.0,0.0],
    '-z+1/6': [0.0,0.0,-1.0,1.0/6.0],
    '-z+1/4': [0.0,0.0,-1.0,1.0/4.0],
    '-z+1/3': [0.0,0.0,-1.0,1.0/3.0],
    '-z+1/2': [0.0,0.0,-1.0,1.0/2.0],
    '-z+2/3': [0.0,0.0,-1.0,2.0/3.0],
    '-z+3/4': [0.0,0.0,-1.0,3.0/4.0],
    '-z+5/6': [0.0,0.0,-1.0,5.0/6.0],
    }
def generate_vector(mystia):
    myvector = []
    decoder = {
    'x-y': [1.0, -1.0, 0.0, 0.0],
    'x-y+1/3': [1.0, -1.0, 0.0, 1.0 / 3.0],
    'x-y+2/3': [1.0, -1.0, 0.0, 2.0 / 3.0],
    'x': [1.0, 0.0, 0.0, 0.0],
    'x+1/4': [1.0, 0.0, 0.0, 1.0 / 4.0],
    'x+1/3': [1.0, 0.0, 0.0, 1.0 / 3.0],
    'x+1/2': [1.0, 0.0, 0.0, 1.0 / 2.0],
    'x+2/3': [1.0, 0.0, 0.0, 2.0 / 3.0],
    'x+3/4': [1.0, 0.0, 0.0, 3.0 / 4.0],
    '-x+y': [-1.0, 1.0, 0.0, 0.0],
    '-x+y+1/3': [-1.0, 1.0, 0.0, 1.0 / 3.0],
    '-x+y+2/3': [-1.0, 1.0, 0.0, 2.0 / 3.0],
    '-x': [-1.0, 0.0, 0.0, 0.0],
    '-x+1/4': [-1.0, 0.0, 0.0, 1.0 / 4.0],
    '-x+1/3': [-1.0, 0.0, 0.0, 1.0 / 3.0],
    '-x+1/2': [-1.0, 0.0, 0.0, 1.0 / 2.0],
    '-x+2/3': [-1.0, 0.0, 0.0, 2.0 / 3.0],
    '-x+3/4': [-1.0, 0.0, 0.0, 3.0 / 4.0],
    'y': [0.0, 1.0, 0.0, 0.0],
    'y+1/4': [0.0, 1.0, 0.0, 1.0 / 4.0],
    'y+1/3': [0.0, 1.0, 0.0, 1.0 / 3.0],
    'y+1/2': [0.0, 1.0, 0.0, 1.0 / 2.0],
    'y+2/3': [0.0, 1.0, 0.0, 2.0 / 3.0],
    'y+3/4': [0.0, 1.0, 0.0, 3.0 / 4.0],
    '-y': [0.0, -1.0, 0.0, 0.0],
    '-y+1/4': [0.0, -1.0, 0.0, 1.0 / 4.0],
    '-y+1/3': [0.0, -1.0, 0.0, 1.0 / 3.0],
    '-y+1/2': [0.0, -1.0, 0.0, 1.0 / 2.0],
    '-y+2/3': [0.0, -1.0, 0.0, 2.0 / 3.0],
    '-y+3/4': [0.0, -1.0, 0.0, 3.0 / 4.0],
    'z': [0.0, 0.0, 1.0, 0.0],
    'z+1/6': [0.0, 0.0, 1.0, 1.0 / 6.0],
    'z+1/4': [0.0, 0.0, 1.0, 1.0 / 4.0],
    'z+1/3': [0.0, 0.0, 1.0, 1.0 / 3.0],
    'z+1/2': [0.0, 0.0, 1.0, 1.0 / 2.0],
    'z+2/3': [0.0, 0.0, 1.0, 2.0 / 3.0],
    'z+3/4': [0.0, 0.0, 1.0, 3.0 / 4.0],
    'z+5/6': [0.0, 0.0, 1.0, 5.0 / 6.0],
    '-z': [0.0, 0.0, -1.0, 0.0],
    '-z+1/6': [0.0, 0.0, -1.0, 1.0 / 6.0],
    '-z+1/4': [0.0, 0.0, -1.0, 1.0 / 4.0],
    '-z+1/3': [0.0, 0.0, -1.0, 1.0 / 3.0],
    '-z+1/2': [0.0, 0.0, -1.0, 1.0 / 2.0],
    '-z+2/3': [0.0, 0.0, -1.0, 2.0 / 3.0],
    '-z+3/4': [0.0, 0.0, -1.0, 3.0 / 4.0],
    '-z+5/6': [0.0, 0.0, -1.0, 5.0 / 6.0],
    }
    for i in string.split(mystia, ','):
        myvector.append(decoder[i])
    return myvector
class symgen:
   
    def cluster_selfcondense(self, pdb):
        returncoord = []
        UC = [0, 0, 0]
        xyz = []
        xyz = pdb.coords()
        orig = [xyz[0], xyz[1], xyz[2], float(pdb.a), float(pdb.b), float(pdb.c)]
        newcoord = [orig[0] + UC[0] * orig[3], orig[1] + UC[1] * orig[4], orig[2] + UC[2] * orig[5], orig[3], orig[4], orig[5]]
        oper = generate_vector('x,y,z')
        returncoord.append(generate_coordinates(oper, newcoord, UC, 'x,y,z'))
        return returncoord
    
    def sg_sym_to_mat_list(self, sgsymbol): 
        result = None
        key = string.strip(string.upper(sgsymbol))
        sym_op = space_groups.get(key,None)
        if sym_op != None:
            result = []
            for op in sym_op:
                mat = []
                for expr in string.split(op,','):

                    mat.append(expr_to_vect[expr])
                mat.append([0.0,0.0,0.0,1.0])

                result.append(mat)
        else:
            if(_feedback(fb_module.symmetry,fb_mask.errors)):
                print "Symmetry-Error: Urecognized space group symbol '"+sgsymbol+"'."
        return result

    def cellbasis(self, angles, edges):
        rad = [radians(i) for i in angles]
        basis = N.identity(4)
        basis[0][1] = cos(rad[2])
        basis[1][1] = sin(rad[2])
        basis[0][2] = cos(rad[1])
        basis[1][2] = (cos(rad[0]) - basis[0][1]*basis[0][2])/basis[1][1]
        basis[2][2] = sqrt(1 - basis[0][2]**2 - basis[1][2]**2)
        edges.append(1.0)
        return basis * edges 


    def findlimits(self,pdb):
        cell_edges = [float(pdb.a),float(pdb.b),float(pdb.c)] #a b c
        cell_angles = [float(pdb.alpha),float(pdb.beta),float(pdb.gamma)] #alpha beta gamma
        spacegroup = pdb.space_group # SG
        basis = self.cellbasis(cell_angles, cell_edges)
        basis = N.matrix(basis)
        center2 = [0.5*((pdb.pdb.max_x)+(pdb.pdb.min_x)),0.5*((pdb.pdb.max_y)+(pdb.pdb.min_y)),0.5*((pdb.pdb.max_z)+(pdb.pdb.min_z))]
        center2=N.matrix(center2 + [1.0]).T
        center_cell2 = basis.I * center2
        center=[pdb.coords()[0],pdb.coords()[1],pdb.coords()[2]] #This actually fills the unit cell as defined by the pdb file 
        
        center = N.matrix(center + [1.0]).T
        center_cell = basis.I * center
        i = 0
        matrices = self.sg_sym_to_mat_list("P1")
        toreturn=[]
        for mat in matrices:
            tonelico = space_groups[pdb.space_group][i]
            i += 1
            mat = N.matrix(mat)
            shift = N.matrix(mat * center_cell)
            test=[]
            for k in shift:
                test.append(math.floor(k))
            shift=N.matrix(test).T
            return [shift[0,0],shift[1,0],shift[2,0]]
            
    def newsympass(self, pdb, matrixx, a, b, c):
        matrices=copy.deepcopy(matrixx)
        #matrices=list(matrixx)
        cell_edges = [float(pdb.a),float(pdb.b),float(pdb.c)] #a b c
        cell_angles = [float(pdb.alpha),float(pdb.beta),float(pdb.gamma)] #alpha beta gamma
        spacegroup = pdb.space_group # SG

        basis = self.cellbasis(cell_angles, cell_edges)
        basis = N.matrix(basis)
        extra_shift = [[float(a)],
                       [float(b)],
                       [float(c)]]
        i = 0
        
        #print t2-t1
        toreturn=[]
        #print len(matrices)
        #print basis
        #print basis.I
        #sys.exit(1)
        #print "%d %d %d"%(a,b,c)
        #print pdb.coords()
        for mat in matrices:
            tonelico = space_groups[pdb.space_group][i]
            i+=1
            mat[0,3]+=extra_shift[0]
            mat[1,3]+=extra_shift[1]
            mat[2,3]+=extra_shift[2]
            
            mat = basis * mat * basis.I
            #print mat
            
            mat_list = list(mat.flat)
            
            toreturn.append(generate_coordinates3(pdb.coords(),mat_list,tonelico,[int(a),int(b),int(c)]))
        #print t2-t1
        #sys.exit(2)
        return toreturn
###THIS IS NEW###
    def timesave(self, pdb, matrices):
        cell_edges = [float(pdb.a),float(pdb.b),float(pdb.c)] #a b c
        cell_angles = [float(pdb.alpha),float(pdb.beta),float(pdb.gamma)] #alpha beta gamma
        spacegroup = pdb.space_group # SG
        basis = self.cellbasis(cell_angles, cell_edges)
        basis = N.matrix(basis)
        center2 = [0.5*((pdb.pdb.max_x)+(pdb.pdb.min_x)),0.5*((pdb.pdb.max_y)+(pdb.pdb.min_y)),0.5*((pdb.pdb.max_z)+(pdb.pdb.min_z))]
        center2=N.matrix(center2 + [1.0]).T
        center_cell2 = basis.I * center2
        center=[pdb.coords()[0],pdb.coords()[1],pdb.coords()[2]] #This actually fills the unit cell as defined by the pdb file
        center = N.matrix(center + [1.0]).T
        center_cell = basis.I * center
        i = 0
        #print basis
        #print basis.I
        #print t2-t1
        toreturn=[]
        for mat in matrices:
            t1=time.clock()
            tonelico = space_groups[pdb.space_group][i]
            i += 1
            mat = N.matrix(mat)
            shift = N.matrix(mat * center_cell2)
            test=[]
            for k in shift:
                if k>0:
                    test.append(math.ceil(k))
                else:
                    test.append(math.floor(k))
            shift=N.matrix(test).T
            shift = N.floor(mat * center_cell2)
            mat[0:3,3]-=shift[0:3,0]
            toreturn.append(mat)
        #print t2-t1
        return toreturn

    def orgsympass(self, pdb, a, b, c):
        cell_edges = [float(pdb.a),float(pdb.b),float(pdb.c)] #a b c
        cell_angles = [float(pdb.alpha),float(pdb.beta),float(pdb.gamma)] #alpha beta gamma
        spacegroup = pdb.space_group # SG
        basis = self.cellbasis(cell_angles, cell_edges)
        basis = N.matrix(basis)
        center2 = [0.5*((pdb.pdb.max_x)+(pdb.pdb.min_x)),0.5*((pdb.pdb.max_y)+(pdb.pdb.min_y)),0.5*((pdb.pdb.max_z)+(pdb.pdb.min_z))]
        center2=N.matrix(center2 + [1.0]).T
        center_cell2 = basis.I * center2
        center=[pdb.coords()[0],pdb.coords()[1],pdb.coords()[2]] #This actually fills the unit cell as defined by the pdb file
        center = N.matrix(center + [1.0]).T
        center_cell = basis.I * center
        extra_shift = [[float(a)],
                       [float(b)],
                       [float(c)]]
        i = 0
        matrices = self.sg_sym_to_mat_list(spacegroup)
        toreturn=[]
        #print "%d %d %d"%(a,b,c)
        #print pdb.coords()
        for mat in matrices:
            tonelico = space_groups[pdb.space_group][i]
            i += 1
            mat = N.matrix(mat)
            shift = N.matrix(mat * center_cell2)
            test=[]
            for k in shift:
                if k>0:
                    test.append(math.ceil(k))
                else:
                    test.append(math.floor(k))
            shift=N.matrix(test).T
            shift = N.floor(mat * center_cell2)
            mat[0:3,3]-=shift[0:3,0]
            mat[0,3]+=extra_shift[0]
            mat[1,3]+=extra_shift[1]
            mat[2,3]+=extra_shift[2]
            mat = basis * mat * basis.I
            #print mat
            mat_list = list(mat.flat)          
            toreturn.append(generate_coordinates3(pdb.coords(),mat_list,tonelico,[int(a),int(b),int(c)]))
        #sys.exit(1)
        return toreturn


    
    
    def varpass(self, a):
        temp=[]       
        limits=self.findlimits(a)
        spacegroup=a.space_group
        t1=time.clock()
        sym_matrix=self.sg_sym_to_mat_list(spacegroup)
        mymatrix=self.timesave(a,sym_matrix)
        for i1 in range(int(limits[0])-1,int(limits[0])+2):
            for j1 in range(int(limits[1])-1,int(limits[1])+2):
                for k1 in range(int(limits[2])-1,int(limits[2])+2):
                    temp.append(self.newsympass(a,mymatrix,i1,j1,k1))
        t2=time.clock()
        #print t2-t1
        return temp

    def transmute(self, coord, oper, UC, pdb):
        a = float(pdb.a)
        b = float(pdb.b)
        c = float(pdb.c)
        xyz = coord
        alpha = math.radians(float(pdb.alpha))
        beta = math.radians(float(pdb.beta))
        gamma = math.radians(float(pdb.gamma))
        if alpha == 0 or beta == 0 or gamma == 0:
            print "No CRYST1 Line Detected for file " + str(pdb.myname) + '\n'
            return [[-999.999, -999.999, -999.999, 'x,y,z', [-2, -2, -2]]]
        vol = a * b * c * sqrt(1-round(cos(alpha), 60) * round(cos(alpha), 60)-round(cos(beta), 60) * round(cos(beta), 60)-round(cos(gamma), 60) * round(cos(gamma), 60) + 2 * b * c * round(cos(alpha), 60) * round(cos(beta), 60) * round(cos(gamma), 60))
        M = matrix([[a, round(b * cos(gamma), 60), round(c * cos(beta), 60)], [0, round(b * sin(gamma), 60), round((c * (cos(alpha)-cos(beta) * cos(gamma))) / sin(gamma), 60)], [0, 0, round(vol / (a * b * sin(gamma)), 60)]])
        M = M.transpose()
        for j1 in range (-1, 2):
            for j2 in range (-1, 2):
                M[j1, j2] = round(M[j1, j2], 60)
        Minv = M.I
        for j1 in range (-1, 2):
            for j2 in range (-1, 2):
                Minv[j1, j2] = round(Minv[j1, j2], 60)
        orig = [float(xyz[0]), float(xyz[1]), float(xyz[2]), M, Minv]
        return generate_coordinates2(generate_vector(oper), orig, UC)

    def varpass2(self, organic):
        toreturn = []
        for o in organic:
            a = self.varpass(o)
            toreturn.append(a)
        return toreturn

    def __init__(self):
        a = 1
