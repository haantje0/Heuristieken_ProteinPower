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

x = 0

'''
fold and give score to proteins
'''

while x < 100:

    backupdirections = deepcopy(hps.directions)
    backupscore = hps.score
    highscore = hps.bestproteins[0]['score']

    for i in range(randint(1,3)):
        newdirections = deepcopy(hps.directions)
        while hps.directions == newdirections:
            newdirectionplace = randint(0,len(hps.directions) - 1)
            newdirection = randint(0,3)
            hps.directions[newdirectionplace] = newdirection

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
