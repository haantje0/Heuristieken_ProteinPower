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
    
def bruteforcer(n):
    if n < (globalvars.lenprotein - 1): 
        globalvars.directions.append(0)
        if n > 0:
            for i in range(4):
   
                if globalvars.directions[n] != 3:
                    if bfproteinchecker() < 0:
                        globalvars.directions[n] += 1
                    else:
                        bruteforcer(n + 1)
                        globalvars.directions[n] += 1 
                   
                else:
                    if bfproteinchecker() < 0:
                        globalvars.directions.pop()
                        return 
                    else:                
                        bruteforcer(n + 1) 
                        globalvars.directions.pop()
        else:
            bruteforcer(n + 1)

    return
    
def hcbruteforcer(n):
    if n < (globalvars.pieceend): 
        globalvars.directions.append(0)
        if n >= globalvars.piecestart:
            for i in range(4):
                
                if globalvars.directions[n - globalvars.piecestart] != 3:
                    if hcpieceproteinchecker() < 0:
                        globalvars.directions[n - globalvars.piecestart] += 1
                    else:
                        hcbruteforcer(n + 1)
                        globalvars.directions[n - globalvars.piecestart] += 1 
                   
                else:
                    if hcpieceproteinchecker() < 0:
                        globalvars.directions.pop()
                        return 
                    else:                
                        hcbruteforcer(n + 1) 
                        globalvars.directions.pop()
        else:
            hcbruteforcer(n + 1)

    return

def hillclimbslicer():
        
    for i in range(len(globalvars.protein) - 5):
        globalvars.piecestart = i
        globalvars.pieceend = i + 5
        hcbruteforcer(i)
        
        if globalvars.bestproteins[0]['score'] >= 2:
            for j in globalvars.bfpiecessaver:
                globalvars.bfpieces.append(j)

        del globalvars.bfpiecessaver[:]
        del globalvars.bestproteins[:]
        
        globalvars.bestproteins = [{'score': -1, 'coordinates': globalvars.coordinates, 'hbonds': globalvars.Hbonds, 'cbonds': globalvars.Cbonds}]
    
def hillclimber():

    while (time.time() - globalvars.start_time) < globalvars.timer:
        
        setdirections()
        
        looper = 0
        cooler = 0    
        
        highscore = 0
        globalvars.counter += 1
        
        globalvars.score = 0
        
        while looper < globalvars.lenprotein*20 and (time.time() - globalvars.start_time) < globalvars.timer:
        
            backupdirections = deepcopy(globalvars.directions)
    
            if globalvars.score > highscore:
                highscore = globalvars.score
            
            random = randint(0, 2)
            if random == 0:     
                newdirections = deepcopy(globalvars.directions)
                while globalvars.directions == newdirections:
                    newdirectionpiece = globalvars.bfpieces[randint(0, len(globalvars.bfpieces) - 1)]

                    for i in range(5):
                        globalvars.directions[newdirectionpiece[0] + i] = newdirectionpiece[1][i]
      
            elif random == 1:
                newdirections = deepcopy(globalvars.directions)
                while globalvars.directions == newdirections:
                    newdirectionplace = randint(0,len(globalvars.directions) - 1)
                    newdirection = randint(0,3)
                    globalvars.directions[newdirectionplace] = newdirection
            
            else:
                newdirectionplace = randint(0,len(globalvars.directions))
                turn = randint(1,3)
                for i in range(len(globalvars.directions) - newdirectionplace):
                    globalvars.directions[newdirectionplace + i] = (globalvars.directions[newdirectionplace + i] + turn) % 4
        
            globalvars.score = hcproteinchecker()
        
            if globalvars.score < 0:
                globalvars.directions = backupdirections
        
            elif globalvars.score > highscore:
                looper = 0
                print "highscore: %i" %highscore
        
            elif globalvars.score < highscore and randint(0, (int (cooler**(2./3.)))) != 0:
                globalvars.directions = backupdirections
        
            elif globalvars.score == highscore and randint(0,1) == 0:
                globalvars.directions = backupdirections
            
            else:
                looper += 1
                cooler += 1
                print looper    

def hcpieceproteinchecker():
    
    del globalvars.Hbonds[:]
    del globalvars.Cbonds[:]

    globalvars.grid.fill("")
    
    score = 0
    
    globalvars.grid[6, 6] = globalvars.protein[globalvars.piecestart]
        
    x = 6
    y = 6
    
    for i in range(len(globalvars.directions)):
            
        if globalvars.directions[i] == 0:
            y -= 1
        elif globalvars.directions[i] == 1:
            x += 1
        elif globalvars.directions[i] == 2:
            y += 1
        elif globalvars.directions[i] == 3:
            x -= 1

        if globalvars.grid[y, x] == "":
            globalvars.grid[y, x] = globalvars.protein[globalvars.piecestart + i + 1]
        else:
            return -1
            
        if globalvars.protein[globalvars.piecestart + i + 1] == "H":
            giveHscore(globalvars.directions[i], x, y)
        elif globalvars.protein[globalvars.piecestart + i + 1] == "C":
            giveHscore(globalvars.directions[i], x, y)
            giveCscore(globalvars.directions[i], x, y)
            
    score = len(globalvars.Hbonds) + 5 * len(globalvars.Cbonds)
    
    if globalvars.bestproteins[0]['score'] == score:
        globalvars.bfpiecessaver.append([globalvars.piecestart, deepcopy(globalvars.directions)])
        
    elif globalvars.bestproteins[0]['score'] < score:
        del globalvars.bestproteins[:]
        del globalvars.bfpiecessaver[:]
        globalvars.bestproteins.append({'score': score})
        globalvars.bfpiecessaver.append([globalvars.piecestart, deepcopy(globalvars.directions)])
            
    return score

def hcproteinchecker():

    del globalvars.Hbonds[:]
    del globalvars.Cbonds[:]
    del globalvars.coordinates[:]

    globalvars.grid.fill("")
    
    score = 0
    
    globalvars.grid[globalvars.lenprotein, globalvars.lenprotein] = globalvars.protein[0]
        
    x = globalvars.lenprotein
    y = globalvars.lenprotein

    globalvars.coordinates.append({'coordinate': ([x,y]),'letter': globalvars.protein[0]})

    for i in range(len(globalvars.directions)):
            
        if globalvars.directions[i] == 0:
            y -= 1
        elif globalvars.directions[i] == 1:
            x += 1
        elif globalvars.directions[i] == 2:
            y += 1
        elif globalvars.directions[i] == 3:
            x -= 1

        if globalvars.grid[y, x] == "":
            globalvars.grid[y, x] = globalvars.protein[i + 1]
            globalvars.coordinates.append({'coordinate': ([x,y]),'letter': globalvars.protein[i + 1]})
        else:
            return -1
            
        if globalvars.protein[i + 1] == "H":
            giveHscore(globalvars.directions[i], x, y)
        elif globalvars.protein[i + 1] == "C":
            giveHscore(globalvars.directions[i], x, y)
            giveCscore(globalvars.directions[i], x, y)
            
    score = len(globalvars.Hbonds) + 5 * len(globalvars.Cbonds)
    
    if globalvars.bestproteins[0]['score'] == score:
        if not any (d['hbonds'] == globalvars.Hbonds for d in globalvars.bestproteins):
            globalvars.bestproteins.append({'score': score, 'coordinates': deepcopy(globalvars.coordinates), 'hbonds': deepcopy(globalvars.Hbonds), 'cbonds': deepcopy(globalvars.Cbonds)})

    elif globalvars.bestproteins[0]['score'] < score:
        del globalvars.bestproteins[:]
        globalvars.bestproteins.append({'score': score, 'coordinates': deepcopy(globalvars.coordinates), 'hbonds': deepcopy(globalvars.Hbonds), 'cbonds': deepcopy(globalvars.Cbonds)})
            
    return score

def bfproteinchecker():

    del globalvars.Hbonds[:]
    del globalvars.Cbonds[:]
    del globalvars.coordinates[:]
    
    globalvars.grid.fill("")

    score = 0.
    
    globalvars.grid[globalvars.lenprotein, globalvars.lenprotein] = globalvars.protein[0]

    Hcount = 0.
    if globalvars.protein[0] == "H":
        Hcount += 1.
        
    Ccount = 0.
    if globalvars.protein[0] == "C":
        Ccount += 1.

    x = globalvars.lenprotein
    y = globalvars.lenprotein
    
    globalvars.coordinates.append({'coordinate': ([x,y]),'letter': globalvars.protein[0]})

    for i in range(len(globalvars.directions)):

        if (Hcount-globalvars.Hprune1)*globalvars.Hprune2 > len(globalvars.Hbonds):
            return -1
            
        if (Ccount-globalvars.Cprune1)*globalvars.Cprune2 > len(globalvars.Cbonds) * 5:
            return -1
            
        if globalvars.directions[i] == 0:
            y -= 1
        elif globalvars.directions[i] == 1:
            x += 1
        elif globalvars.directions[i] == 2:
            y += 1
        elif globalvars.directions[i] == 3:
            x -= 1

        if globalvars.grid[y, x] == "":
            globalvars.grid[y, x] = globalvars.protein[i + 1]
            globalvars.coordinates.append({'coordinate': ([x,y]),'letter': globalvars.protein[i + 1]})
        else:
            return -1

        if globalvars.protein[i + 1] == "H":
            giveHscore(globalvars.directions[i], x, y)
            Hcount += 1.
        elif globalvars.protein[i + 1] == "C":
            giveHscore(globalvars.directions[i], x, y)
            giveCscore(globalvars.directions[i], x, y)
            Ccount += 1.
            
    score = len(globalvars.Hbonds) + 5 * len(globalvars.Cbonds)
    
    if len(globalvars.directions) == globalvars.lenprotein - 1:
        if globalvars.bestproteins[0]['score'] == score:
            if not any (d['hbonds'] == globalvars.Hbonds for d in globalvars.bestproteins):
                globalvars.bestproteins.append({'score': score, 'coordinates': deepcopy(globalvars.coordinates), 'hbonds': deepcopy(globalvars.Hbonds), 'cbonds': deepcopy(globalvars.Cbonds)})
                elapsed_time = time.time() - globalvars.start_time
                print "elapsed time: %f seconds" %elapsed_time
                if Ccount > 0.:
                    print "Cprune: %f" %(len(globalvars.Cbonds)*5/(Ccount-globalvars.Cprune1))
                print "Hprune: %f" %(len(globalvars.Hbonds)/(Hcount-globalvars.Hprune1))
                printprotein(globalvars.bestproteins[-1])

        elif globalvars.bestproteins[0]['score'] < score:
            del globalvars.bestproteins[:]
            globalvars.bestproteins.append({'score': score, 'coordinates': deepcopy(globalvars.coordinates), 'hbonds': deepcopy(globalvars.Hbonds), 'cbonds': deepcopy(globalvars.Cbonds)})
            elapsed_time = time.time() - globalvars.start_time
            print "elapsed time: %f seconds" %elapsed_time
            if Ccount > 0.:
                print "Cprune: %f" %(len(globalvars.Cbonds)*5/(Ccount-globalvars.Cprune1))
            print "Hprune: %f" %(len(globalvars.Hbonds)/(Hcount-globalvars.Hprune1))
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
    