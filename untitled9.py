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

start_time = time.time()

proteinstring = "HPHPPHHPPHHPPPHPHPHPHPHPHHPH"

protein = []

for i in proteinstring:
    protein.append(i)

lenprotein = len(protein)

gridlength = 2 * lenprotein + 1

grid = np.chararray((gridlength, gridlength))

Hbonds = []

directions = []

for i in range(lenprotein - 1):
    directions.append(0)

coordinates = [{'coordinate': ([0,0]),'letter': ""}]

bestproteins = [{'score': 0, 'coordinates': coordinates}]

#for i in protein[0:-1]:
#    directions.append(0)

def proteinchecker():
            
    global bestproteins  
    global coordinates
    global Hbonds
    
    del Hbonds[:]
    del coordinates[:]
    
    grid.fill("")
    
    score = 0    
    
    grid[lenprotein, lenprotein] = protein[0]

    x = lenprotein
    y = lenprotein
    
    coordinates.append({'coordinate': ([x,y]),'letter': protein[0]})
    
    for i in range(len(directions)):
        
        if directions[i] == 0:
            y -= 1
        elif directions[i] == 1:
            x += 1  
        elif directions[i] == 2:
            y += 1
        elif directions[i] == 3:
            x -= 1

        if grid[y, x] == "":
            grid[y, x] = protein[i + 1]
            coordinates.append({'coordinate': ([x,y]),'letter': protein[i + 1]})
        else:
            return -1
        
        if protein[i + 1] == "H":
            score += givescore(directions[i], x, y)

    if bestproteins[0]['score'] == score:
        if not any (d['coordinates'] == coordinates for d in bestproteins):
            bestproteins.append({'score': score, 'coordinates': coordinates})
    elif bestproteins[0]['score'] < score:
        del bestproteins[:]        
        bestproteins.append({'score': score, 'coordinates': coordinates})
    
    return score


def givescore(direction, x, y):
    points = 0
    
    if direction != 3:
        if grid[y, x + 1] == "H":
            points += 1
            Hbonds.append([[x, x + 1],[y, y]])
    if direction != 1:
        if grid[y, x - 1] == "H":
            points += 1
            Hbonds.append([[x, x - 1],[y, y]])
    if direction != 2:
        if grid[y - 1, x] == "H":
            points += 1
            Hbonds.append([[x, x],[y, y - 1]])
    if direction != 0:
        if grid[y + 1, x] == "H":
            points += 1
            Hbonds.append([[x, x],[y, y + 1]])
    return points

x = 0

while x < 10000:
    
    backupdirections = deepcopy(directions)
    #backupscore = score
    
    newdirectionplace = randint(0,len(directions) - 1)
    newdirection = randint(0,3)
    directions[newdirectionplace] = newdirection    
    
    score = proteinchecker()

    if score < 0:
        directions = backupdirections
    else:
        x += 1
    

'''
print and plot the protein(s)
'''


elapsed_time = time.time() - start_time

print
print "elapsed time: %f seconds" %elapsed_time
print "this protein has a score of: %i" %bestproteins[0]['score']
print "there are %i proteins with this score" %len(bestproteins)
print

color = {'H': 'lightgreen', 'P': 'lightblue'}
for j in bestproteins:
    linex = []
    liney = []
    
    #for j in bestproteins:
    for i in j['coordinates']:
        plt.scatter(i['coordinate'][0],i['coordinate'][1], s=1000, c=color[i['letter']], zorder=2)
        plt.annotate(i['letter'], (i['coordinate'][0],i['coordinate'][1]), zorder=2)
        linex.append(i['coordinate'][0])
        liney.append(i['coordinate'][1])
    
    for i in Hbonds:
        plt.plot(i[0], i[1], zorder = 1, lw=3, c='red', ls='dotted')
    
    plt.plot(linex, liney, zorder=1, lw=3, c='black')
    
    plt.axis('off')
    plt.show()