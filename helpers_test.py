import matplotlib.pyplot as plt
import time
import numpy as np
from copy import deepcopy
from random import randint

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
            helpers.givescore(directions[i], x, y)

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
