import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
from random import randint
import time
import Protein_library as Plib
import globalvariables as globalvars

def setprotein():

    proteinnumber = 10

    while proteinnumber < 0 or proteinnumber > 8:
        try:
            proteinnumber = int(raw_input("The protein you want to use (integer between 0 and 8): "))
        except ValueError:
            print("Please enter a number between 0 and 8 (check the library)")
    
    proteinsequence = Plib.list[proteinnumber]
    
    for i in proteinsequence:
        globalvars.protein.append(i)

    globalvars.lenprotein = len(globalvars.protein)
    
    gridlength = 2 * globalvars.lenprotein + 1

    globalvars.grid = np.chararray((gridlength, gridlength))

def settimer():
    
    while True:
        try:
            globalvars.timer = int(raw_input("Please give a looping timer (in seconds): "))
            globalvars.start_time = time.time()
        except ValueError:
            print("Please give it in seconds!")
            continue
        else:
            break

def setprune():

    while globalvars.Hprune1 < 0.:
        try:
            globalvars.Hprune1 = float(raw_input("After how manny \"H\" do you want to prune? "))
        except ValueError:
            print("please enter a positive number")
            
    while globalvars.Hprune2 < 0.:
        try:
            globalvars.Hprune2 = float(raw_input("What should the average score of \"H\" be? "))
        except ValueError:
            print("please enter a positive number")
            
    while globalvars.Cprune1 < 0.:
        try:
            globalvars.Cprune1 = float(raw_input("After how manny \"C\" do you want to prune? "))
        except ValueError:
            print("please enter a positive number")
            
    while globalvars.Cprune2 < 0.:
        try:
            globalvars.Cprune2 = float(raw_input("What should the average score of \"C\" be? "))
        except ValueError:
            print("please enter a positive number")
    
def setdirections():
    score = -1
    while score < 0:
        del globalvars.directions[:]
        prevdirection = 0
        
        for i in range(globalvars.lenprotein - 1):
            newdirection = randint(0,3)
            while newdirection == (prevdirection + 2) % 4:
                newdirection = randint(0,3)
                
            globalvars.directions.append(newdirection)
            prevdirection = newdirection
            
        score = hcproteinchecker()
        print score 
    
def proteinchecker():
    del globalvars.Hbonds[:]
    del globalvars.Cbonds[:]
    del globalvars.coordinates[:]
    
    globalvars.grid.fill("")

    score = 0.
    
    globalvars.grid[globalvars.lenprotein, globalvars.lenprotein] = globalvars.protein[0 + globalvars.piecestart]

    globalvars.Hcount = 0.
    if globalvars.protein[0] == "H":
        globalvars.Hcount += 1.
        
    globalvars.Ccount = 0.
    if globalvars.protein[0] == "C":
        globalvars.Ccount += 1.

    globalvars.x = globalvars.lenprotein
    globalvars.y = globalvars.lenprotein
    
    globalvars.coordinates.append({'coordinate': ([globalvars.x,globalvars.y]),'letter': globalvars.protein[0]})

    for i in range(len(globalvars.directions)):

        if (globalvars.Hcount-globalvars.Hprune1)*globalvars.Hprune2 > len(globalvars.Hbonds):
            return -1
            
        if (globalvars.Ccount-globalvars.Cprune1)*globalvars.Cprune2 > len(globalvars.Cbonds) * 5:
            return -1
            
        if globalvars.directions[i] == 0:
            globalvars.y -= 1
        elif globalvars.directions[i] == 1:
            globalvars.x += 1
        elif globalvars.directions[i] == 2:
            globalvars.y += 1
        elif globalvars.directions[i] == 3:
            globalvars.x -= 1
   
        if globalvars.grid[globalvars.y, globalvars.x] == "":
            globalvars.grid[globalvars.y, globalvars.x] = globalvars.protein[i + globalvars.piecestart + 1]
            globalvars.coordinates.append({'coordinate': ([globalvars.x,globalvars.y]),'letter': globalvars.protein[i + globalvars.piecestart + 1]})
        else:
            return -1

        if globalvars.protein[i + globalvars.piecestart + 1] == "H":
            giveHscore(globalvars.directions[i], globalvars.x, globalvars.y)
            globalvars.Hcount += 1.
        elif globalvars.protein[i + globalvars.piecestart + 1] == "C":
            giveHscore(globalvars.directions[i], globalvars.x, globalvars.y)
            giveCscore(globalvars.directions[i], globalvars.x, globalvars.y)
            globalvars.Ccount += 1.
            
    score = len(globalvars.Hbonds) + 5 * len(globalvars.Cbonds)
    
    return score
    
def hcpieceproteinchecker():
    
    score = proteinchecker()
    
    if globalvars.bfpiecessaver[0][2] == score:
        globalvars.bfpiecessaver.append([globalvars.piecestart, deepcopy(globalvars.directions), score])
        
    elif globalvars.bfpiecessaver[0][2] < score:
        del globalvars.bfpiecessaver[:]
        globalvars.bfpiecessaver.append([globalvars.piecestart, deepcopy(globalvars.directions), score])
    
    return score
            
def hcproteinchecker():
    score = proteinchecker()

    if globalvars.bestproteins[0]['score'] == score:
        if not any (d['hbonds'] == globalvars.Hbonds for d in globalvars.bestproteins):
            globalvars.bestproteins.append({'score': score, 'coordinates': deepcopy(globalvars.coordinates), 'hbonds': deepcopy(globalvars.Hbonds), 'cbonds': deepcopy(globalvars.Cbonds)})

    elif globalvars.bestproteins[0]['score'] < score:
        del globalvars.bestproteins[:]
        globalvars.bestproteins.append({'score': score, 'coordinates': deepcopy(globalvars.coordinates), 'hbonds': deepcopy(globalvars.Hbonds), 'cbonds': deepcopy(globalvars.Cbonds)})
            
    return score
    
def bfproteinchecker():
    score = proteinchecker()

    if len(globalvars.directions) == globalvars.lenprotein - 1:
        if globalvars.bestproteins[0]['score'] == score:
            if not any (d['hbonds'] == globalvars.Hbonds for d in globalvars.bestproteins):
                globalvars.bestproteins.append({'score': score, 'coordinates': deepcopy(globalvars.coordinates), 'hbonds': deepcopy(globalvars.Hbonds), 'cbonds': deepcopy(globalvars.Cbonds)})
                elapsed_time = time.time() - globalvars.start_time
                print "elapsed time: %f seconds" %elapsed_time
                if globalvars.Ccount > 0.:
                    print "Cprune: %f" %(len(globalvars.Cbonds)*5/(globalvars.Ccount-globalvars.Cprune1))
                print "Hprune: %f" %(len(globalvars.Hbonds)/(globalvars.Hcount-globalvars.Hprune1))
                printprotein(globalvars.bestproteins[-1])

        elif globalvars.bestproteins[0]['score'] < score:
            del globalvars.bestproteins[:]
            globalvars.bestproteins.append({'score': score, 'coordinates': deepcopy(globalvars.coordinates), 'hbonds': deepcopy(globalvars.Hbonds), 'cbonds': deepcopy(globalvars.Cbonds)})
            elapsed_time = time.time() - globalvars.start_time
            print "elapsed time: %f seconds" %elapsed_time
            if globalvars.Ccount > 0.:
                print "Cprune: %f" %(len(globalvars.Cbonds)*5/(globalvars.Ccount-globalvars.Cprune1))
            print "Hprune: %f" %(len(globalvars.Hbonds)/(globalvars.Hcount-globalvars.Hprune1))
            plotter()

    return score
    
def giveHscore(direction, x, y):
    if direction != 3:
        if globalvars.grid[y, x + 1] == "H":
            globalvars.Hbonds.append([[x, x + 1],[y, y]])
    if direction != 1:
        if globalvars.grid[y, x - 1] == "H":
            globalvars.Hbonds.append([[x, x - 1],[y, y]])
    if direction != 2:
        if globalvars.grid[y - 1, x] == "H":
            globalvars.Hbonds.append([[x, x],[y, y - 1]])
    if direction != 0:
        if globalvars.grid[y + 1, x] == "H":
            globalvars.Hbonds.append([[x, x],[y, y + 1]])
    return

def giveCscore(direction, x, y):
    if direction != 3:
        if globalvars.grid[y, x + 1] == "C":
            globalvars.Cbonds.append([[x, x + 1],[y, y]])
    if direction != 1:
        if globalvars.grid[y, x - 1] == "C":
            globalvars.Cbonds.append([[x, x - 1],[y, y]])
    if direction != 2:
        if globalvars.grid[y - 1, x] == "C":
            globalvars.Cbonds.append([[x, x],[y, y - 1]])
    if direction != 0:
        if globalvars.grid[y + 1, x] == "C":
            globalvars.Cbonds.append([[x, x],[y, y + 1]])
    return

def plotter():
    for j in globalvars.bestproteins:
        printprotein(j)
    return   
    
def printprotein(j):
    color = {'H': 'lightgreen', 'P': 'lightblue', 'C': 'pink'}
    
    linex = []
    liney = []
    for i in j['coordinates']:
        plt.scatter(i['coordinate'][0],i['coordinate'][1], s=10000/globalvars.lenprotein, c=color[i['letter']], zorder=2)
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
    