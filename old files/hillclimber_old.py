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

proteinstring = "HHPHPHPHPHHHHPHPPPHPPPHPP"

protein = []

for i in proteinstring:
    protein.append(i)


lenprotein = len(protein)

gridlength = 2 * lenprotein + 1

grid = np.chararray((gridlength, gridlength))

Hbonds = []

directions = []

directionssaver = []

score = -1        
                
coordinates = [{'coordinate': ([0,0]),'letter': ""}]

bestproteins = [{'score': score, 'coordinates': coordinates, 'hbonds': [], 'directions': []}]

def proteinchecker():
            
    global bestproteins  
    global coordinates
    global Hbonds
    global directionssaver
    
    del Hbonds[:]
    del coordinates[:]
    
    grid.fill("")
        
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
            givescore(directions[i], x, y)

    score = len(Hbonds)

    if bestproteins[0]['score'] == score:
        if not any (d['hbonds'] == Hbonds for d in bestproteins):
            bestproteins.append({'score': score, 'coordinates': deepcopy(coordinates), 'hbonds': deepcopy(Hbonds), 'directions': deepcopy(directions)})
            directionssaver = deepcopy(directions)

    elif bestproteins[0]['score'] < score:
        del bestproteins[:]  
        bestproteins.append({'score': score, 'coordinates': deepcopy(coordinates), 'hbonds': deepcopy(Hbonds), 'directions': deepcopy(directions)})
        directionssaver = deepcopy(directions)

    return score


def givescore(direction, x, y):
    
    if direction != 3:
        if grid[y, x + 1] == "H":
            Hbonds.append([[x, x + 1],[y, y]])
    if direction != 1:
        if grid[y, x - 1] == "H":
            Hbonds.append([[x, x - 1],[y, y]])
    if direction != 2:
        if grid[y - 1, x] == "H":
            Hbonds.append([[x, x],[y, y - 1]])
    if direction != 0:
        if grid[y + 1, x] == "H":
            Hbonds.append([[x, x],[y, y + 1]])
    return

if lenprotein <= 25:
    while score < 0:
        del directions[:]
        for i in range(lenprotein - 1):
            directions.append(randint(0,3))
        score = proteinchecker()
        print score
else:
    for i in range(lenprotein - 1):
        directions.append(0)
        
x = 0

while x < 100:
    
    backupdirections = deepcopy(directions)
    backupscore = score
    highscore = bestproteins[0]['score']
    
    for i in range(randint(1,3)):
        newdirections = deepcopy(directions)
        while directions == newdirections:
            newdirectionplace = randint(0,len(directions) - 1)
            newdirection = randint(0,3)
            directions[newdirectionplace] = newdirection
    
    score = proteinchecker()
    
    if score < 0:
        directions = backupdirections
        
    elif score > highscore:
        x = 0  
        print x

    elif score <= bestproteins[0]['score'] and randint(0, 100) != 0:
        directions = backupdirections

    else:
        x += 1
        print x


'''
print and plot the protein(s)
'''


elapsed_time = time.time() - start_time

print
print "elapsed time: %i seconds" %elapsed_time
print "these proteins have a score of: %i" %bestproteins[0]['score']
print "there are %i proteins with this score" %len(bestproteins)
print

color = {'H': 'lightgreen', 'P': 'lightblue'}
for j in bestproteins:
    linex = []
    liney = []
    #for j in bestproteins:
    for i in j['coordinates']:
        plt.scatter(i['coordinate'][0],i['coordinate'][1], s=10000/lenprotein, c=color[i['letter']], zorder=2)
        plt.annotate(i['letter'], (i['coordinate'][0],i['coordinate'][1]), zorder=2)
        linex.append(i['coordinate'][0])
        liney.append(i['coordinate'][1])
    
    for i in j['hbonds']:
        plt.plot(i[0], i[1], zorder = 1, lw=3, c='red', ls='dotted')
    
    plt.plot(linex, liney, zorder=1, lw=3, c='black')
    
    plt.title('Protein with a score of: %i' %j['score'])
    plt.axis('off')
    plt.show()