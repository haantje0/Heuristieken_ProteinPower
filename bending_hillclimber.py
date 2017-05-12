# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 13:59:41 2017

@author: lex
"""

import matplotlib.pyplot as plt
import time
import numpy as np
from copy import deepcopy
from random import randint
import helpers as hps

start_time = time.time()

'''
initialize protein
'''

if hps.lenprotein <= 25:
    while hps.score < 0:
        del hps.directions[:]
        for i in range(hps.lenprotein - 1):
            hps.directions.append(randint(0,3))
        hps.score = hps.proteinchecker()
        print hps.score
else:
    for i in range(hps.lenprotein - 1):
        hps.directions.append(0)

'''
fold and give score to proteins
'''

x = 0

print "START"

while x < 100:

    backupdirections = deepcopy(hps.directions)
    backupscore = hps.score
    highscore = hps.bestproteins[0]['score']

    newdirectionplace = randint(0,len(hps.directions))
    turn = randint(1,3)

    for i in range(len(hps.directions) - newdirectionplace):
        hps.directions[newdirectionplace + i] = (hps.directions[newdirectionplace + i] + turn) % 4

    hps.score = hps.proteinchecker()

    if hps.score < 0:
        hps.directions = backupdirections

    elif hps.score > highscore:
        x = 0
        print x

    elif hps.score <= hps.bestproteins[0]['score'] and randint(0, 100) != 0:
        hps.directions = backupdirections

    else:
        x += 1
        print x


'''
print and plot the protein(s)
'''

elapsed_time = time.time() - start_time

hps.plotter(elapsed_time)
