import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
from random import randint
import time

start_time = time.time()

protein = []

lenprotein = 0

gridlength = 0

Hprune1 = 0.
Hprune2 = 0.

Cprune1 = 0.
Cprune2 = 0.

grid = np.chararray(1, 1)

Hbonds = []
Cbonds = []

score = -1.

counter = 0

directions = []

coordinates = [{'coordinate': ([0,0]),'letter': ""}]

bestproteins = [{'score': score, 'coordinates': coordinates, 'hbonds': []}]

def setprotein(string):
    for i in string:
        protein.append(i)

    global lenprotein
    global gridlength   
    global grid

    lenprotein = len(protein)
    
    gridlength = 2 * lenprotein + 1

    grid = np.chararray((gridlength, gridlength))

def setprune(HPrune1, HPrune2, CPrune1, CPrune2):
    global Hprune1
    global Hprune2
    
    global Cprune1
    global Cprune2

    Hprune1 = HPrune1
    Hprune2 = HPrune2

    Cprune1 = CPrune1
    Cprune2 = CPrune2

def bruteforcer(n):
    if n < (lenprotein - 1): 
        directions.append(0)
        if n > 0:
            for i in range(4):
   
                if directions[n] != 3:
                    if bfproteinchecker() < 0:
                        directions[n] += 1
                    else:
                        bruteforcer(n + 1)
                        directions[n] += 1 
                   
                else:
                    if bfproteinchecker() < 0:
                        directions.pop()
                        return 
                    else:                
                        bruteforcer(n + 1) 
                        directions.pop()
        else:
            bruteforcer(n + 1)

    return
    
def hillclimber(timer):
    
    global counter 
    global directions
    
    while (time.time() - start_time) < timer:
        
        setdirections()
        
        x = 0
        y = 0    
        
        highscore = 0
        counter += 1
        
        score = 0
        
        while x < lenprotein*20 and (time.time() - start_time) < timer:
        
            backupdirections = deepcopy(directions)
    
            if score > highscore:
                highscore = score
            
            for i in range(randint(1,1)):
                newdirections = deepcopy(directions)
                while directions == newdirections:
                    newdirectionplace = randint(0,len(directions) - 1)
                    newdirection = randint(0,3)
                    directions[newdirectionplace] = newdirection
        
            score = hcproteinchecker()
        
            if score < 0:
                directions = backupdirections
        
            elif score > highscore:
                x = 0
                print "highscore: %i" %highscore
        
            elif score < highscore and randint(0, (int (y**(2./3.)))) != 0:
                directions = backupdirections
        
            elif score == highscore and randint(0,1) == 0:
                directions = backupdirections
            
            else:
                x += 1
                y += 1
                print x    
    
def hcproteinchecker():

    global bestproteins
    global coordinates
    global Hbonds
    global directionssaver

    del Hbonds[:]
    del Cbonds[:]
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
            giveHscore(directions[i], x, y)
        elif protein[i + 1] == "C":
            giveHscore(directions[i], x, y)
            giveCscore(directions[i], x, y)
            
    score = len(Hbonds) + 5 * len(Cbonds)
    
    if bestproteins[0]['score'] == score:
        if not any (d['hbonds'] == Hbonds for d in bestproteins):
            bestproteins.append({'score': score, 'coordinates': deepcopy(coordinates), 'hbonds': deepcopy(Hbonds), 'cbonds': deepcopy(Cbonds)})

    elif bestproteins[0]['score'] < score:
        del bestproteins[:]
        bestproteins.append({'score': score, 'coordinates': deepcopy(coordinates), 'hbonds': deepcopy(Hbonds), 'cbonds': deepcopy(Cbonds)})
            
    return score

def bfproteinchecker():

    global bestproteins
    global coordinates
    global Hbonds
    global directionssaver

    del Hbonds[:]
    del Cbonds[:]
    del coordinates[:]
    
    grid.fill("")

    score = 0.
    
    grid[lenprotein, lenprotein] = protein[0]

    Hcount = 0.
    if protein[0] == "H":
        Hcount += 1.
        
    Ccount = 0.
    if protein[0] == "C":
        Ccount += 1.

    x = lenprotein
    y = lenprotein
    
    coordinates.append({'coordinate': ([x,y]),'letter': protein[0]})

    for i in range(len(directions)):

        if (Hcount-Hprune1)*Hprune2 > len(Hbonds):
            return -1
            
        if (Ccount-Cprune1)*Cprune2 > len(Cbonds) * 5:
            return -1
            
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
            giveHscore(directions[i], x, y)
            Hcount += 1.
        elif protein[i + 1] == "C":
            giveHscore(directions[i], x, y)
            giveCscore(directions[i], x, y)
            Ccount += 1.
            
    score = len(Hbonds) + 5 * len(Cbonds)
    
    if len(directions) == lenprotein - 1:
        if bestproteins[0]['score'] == score:
            if not any (d['hbonds'] == Hbonds for d in bestproteins):
                bestproteins.append({'score': score, 'coordinates': deepcopy(coordinates), 'hbonds': deepcopy(Hbonds), 'cbonds': deepcopy(Cbonds)})
                elapsed_time = time.time() - start_time
                print "elapsed time: %f seconds" %elapsed_time
                print "Cprune: %f" %(len(Cbonds)*5/(Ccount-Cprune1))
                print "Hprune: %f" %(len(Hbonds)/(Hcount-Hprune1))
                printprotein(bestproteins[-1])

        elif bestproteins[0]['score'] < score:
            del bestproteins[:]
            bestproteins.append({'score': score, 'coordinates': deepcopy(coordinates), 'hbonds': deepcopy(Hbonds), 'cbonds': deepcopy(Cbonds)})
            elapsed_time = time.time() - start_time
            print "elapsed time: %f seconds" %elapsed_time
            print "Cprune: %f" %(len(Cbonds)*5/(Ccount-Cprune1))
            print "Hprune: %f" %(len(Hbonds)/(Hcount-Hprune1))
            plotter()

    return score
    
def giveHscore(direction, x, y):
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

def giveCscore(direction, x, y):
    if direction != 3:
        if grid[y, x + 1] == "C":
            Cbonds.append([[x, x + 1],[y, y]])
    if direction != 1:
        if grid[y, x - 1] == "C":
            Cbonds.append([[x, x - 1],[y, y]])
    if direction != 2:
        if grid[y - 1, x] == "C":
            Cbonds.append([[x, x],[y, y - 1]])
    if direction != 0:
        if grid[y + 1, x] == "C":
            Cbonds.append([[x, x],[y, y + 1]])
    return

def setdirections():
    score = -1
    while score < 0:
        del directions[:]
        prevdirection = 0
        
        for i in range(lenprotein - 1):
            newdirection = randint(0,3)
            while newdirection == (prevdirection + 2) % 4:
                newdirection = randint(0,3)
                
            directions.append(newdirection)
            prevdirection = newdirection
            
        score = hcproteinchecker()
        print score

def plotter():
    for j in bestproteins:
        printprotein(j)
    return

def printprotein(j):
    color = {'H': 'lightgreen', 'P': 'lightblue', 'C': 'pink'}
    
    linex = []
    liney = []
    for i in j['coordinates']:
        plt.scatter(i['coordinate'][0],i['coordinate'][1], s=10000/lenprotein, c=color[i['letter']], zorder=2)
        plt.annotate(i['letter'], (i['coordinate'][0],i['coordinate'][1]), zorder=2)
        linex.append(i['coordinate'][0])
        liney.append(i['coordinate'][1])

    for i in j['hbonds']:
        plt.plot(i[0], i[1], zorder = 1, lw=3, c='red', ls='dotted')
        
    for i in j['cbonds']:
        plt.plot(i[0], i[1], zorder = 1, lw=5, c='purple', ls='dotted')

    plt.plot(linex, liney, zorder=1, lw=3, c='black')
    plt.axis('off')
    plt.title('Protein with a score of: %i' %j['score'])
    plt.show()