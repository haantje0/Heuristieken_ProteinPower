import time
import numpy as np
from copy import deepcopy

proteinstring = "HHPHHHPH"
protein = []

for i in proteinstring:
    protein.append(i)

lenprotein = len(protein)

gridlength = 2 * lenprotein + 1

grid = np.chararray((gridlength, gridlength))

directions = []

bestproteins = [{'grid': grid, 'score': 0}]

def placer():
    for i in protein[0:-1]:
        directions.append(0)

def recursion(n):
    if len(directions) - n > 0:
        recursion(n + 1)
        for i in range(4):

            if directions[n] != 3:
                directions[n] += 1
                proteinplacer()
                recursion(n + 1)

            else:
                directions[n] = 0
                return

def bruteforcer(n):
    if n >= 1:
        for i in range(4):

            if directions[n] != 3:
                directions[n] += 1
                proteinplacer()
                recursion(n + 1)

            else:
                directions[n] = 0
                bruteforcer(n - 1)
    return

def proteinplacer():

    global bestproteins

    grid.fill("")

    score = 0

    grid[lenprotein, lenprotein] = protein[0]

    x = lenprotein
    y = lenprotein
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
        else:
            return

        if protein[i + 1] == "H":
            score += givescore(directions[i], x, y)


    if bestproteins[0]['score'] == score:
        bestproteins.append({'grid': deepcopy(grid), 'score': score})
    elif bestproteins[0]['score'] < score:
        del bestproteins[:]
        bestproteins.append({'grid': deepcopy(grid), 'score': score})

    return

def givescore(direction, x, y):
    points = 0

    if direction != 3:
        if grid[y, x + 1] == "H":
            points += 1
    if direction != 1:
        if grid[y, x - 1] == "H":
            points += 1
    if direction != 2:
        if grid[y - 1, x] == "H":
            points += 1
    if direction != 0:
        if grid[y + 1, x] == "H":
            points += 1
    return points

def plotter():
    for i in bestproteins:
        print i['grid']
        print "score: %i" %i['score']
        print
