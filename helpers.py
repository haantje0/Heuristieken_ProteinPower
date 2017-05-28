import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
from random import randint
import time
import Protein_library as Plib

start_time = time.time()

protein = []

lenprotein = 0

gridlength = 0

Hprune1 = -1.
Hprune2 = -1.

Cprune1 = -1.
Cprune2 = -1.

grid = np.chararray(1, 1)

Hbonds = []
Cbonds = []

score = -1.

counter = 0
timer = 0

bfpiecessaver = []
bfpieces = []
piecestart = 0
pieceend = 0

directions = []

coordinates = [{'coordinate': ([0,0]),'letter': "P"}]

bestproteins = [{'score': score, 'coordinates': coordinates, 'hbonds': Hbonds, 'cbonds': Cbonds}]

def setprotein():

    proteinnumber = 10

    while proteinnumber < 0 or proteinnumber > 8:
        try:
            proteinnumber = int(raw_input("The protein you want to use (integer between 0 and 8): "))
        except ValueError:
            print("Please enter a number between 0 and 8 (check the library)")
    
    proteinsequence = Plib.list[proteinnumber]
    
    for i in proteinsequence:
        protein.append(i)

    global lenprotein
    global gridlength   
    global grid

    lenprotein = len(protein)
    
    gridlength = 2 * lenprotein + 1

    grid = np.chararray((gridlength, gridlength))

def settimer():
    global timer  
    global start_time
    
    while True:
        try:
            timer = int(raw_input("Please give a looping timer (in seconds): "))
            start_time = time.time()
        except ValueError:
            print("Please give it in seconds!")
            continue
        else:
            break

def setprune():
    global Hprune1
    global Hprune2
    
    global Cprune1
    global Cprune2

    while Hprune1 < 0.:
        try:
            Hprune1 = float(raw_input("After how manny \"H\" do you want to prune? "))
        except ValueError:
            print("please enter a positive number")
            
    while Hprune2 < 0.:
        try:
            Hprune2 = float(raw_input("What should the average score of \"H\" be? "))
        except ValueError:
            print("please enter a positive number")
            
    while Cprune1 < 0.:
        try:
            Cprune1 = float(raw_input("After how manny \"C\" do you want to prune? "))
        except ValueError:
            print("please enter a positive number")
            
    while Cprune2 < 0.:
        try:
            Cprune2 = float(raw_input("What should the average score of \"C\" be? "))
        except ValueError:
            print("please enter a positive number")
    
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
    
def hcbruteforcer(n):
    if n < (pieceend): 
        directions.append(0)
        if n >= piecestart:
            for i in range(4):
                
                if directions[n - piecestart] != 3:
                    if hcpieceproteinchecker() < 0:
                        directions[n - piecestart] += 1
                    else:
                        hcbruteforcer(n + 1)
                        directions[n - piecestart] += 1 
                   
                else:
                    if hcpieceproteinchecker() < 0:
                        directions.pop()
                        return 
                    else:                
                        hcbruteforcer(n + 1) 
                        directions.pop()
        else:
            hcbruteforcer(n + 1)

    return

def hillclimbslicer():
    global piecestart
    global pieceend
    global bfpiecessaver
    global bfpieces
    
    global bestproteins
        
    for i in range(len(protein) - 5):
        piecestart = i
        pieceend = i + 5
        hcbruteforcer(i)
        
        if bestproteins[0]['score'] >= 2:
            for j in bfpiecessaver:
                bfpieces.append(j)

        del bfpiecessaver[:]
        del bestproteins[:]
        
        bestproteins = [{'score': -1, 'coordinates': coordinates, 'hbonds': Hbonds, 'cbonds': Cbonds}]
    
def hillclimber():
    
    global counter 
    global directions
    
    while (time.time() - start_time) < timer:
        
        setdirections()
        
        looper = 0
        cooler = 0    
        
        highscore = 0
        counter += 1
        
        score = 0
        
        while looper < lenprotein*20 and (time.time() - start_time) < timer:
        
            backupdirections = deepcopy(directions)
    
            if score > highscore:
                highscore = score
            
            random = randint(0, 2)
            if random == 0:     
                newdirections = deepcopy(directions)
                while directions == newdirections:
                    newdirectionpiece = bfpieces[randint(0, len(bfpieces) - 1)]

                    for i in range(5):
                        directions[newdirectionpiece[0] + i] = newdirectionpiece[1][i]
      
            elif random == 1:
                newdirections = deepcopy(directions)
                while directions == newdirections:
                    newdirectionplace = randint(0,len(directions) - 1)
                    newdirection = randint(0,3)
                    directions[newdirectionplace] = newdirection
            
            else:
                newdirectionplace = randint(0,len(directions))
                turn = randint(1,3)
                for i in range(len(directions) - newdirectionplace):
                    directions[newdirectionplace + i] = (directions[newdirectionplace + i] + turn) % 4
        
            score = hcproteinchecker()
        
            if score < 0:
                directions = backupdirections
        
            elif score > highscore:
                looper = 0
                print "highscore: %i" %highscore
        
            elif score < highscore and randint(0, (int (cooler**(2./3.)))) != 0:
                directions = backupdirections
        
            elif score == highscore and randint(0,1) == 0:
                directions = backupdirections
            
            else:
                looper += 1
                cooler += 1
                print looper    

def hcpieceproteinchecker():
    
    global bfpiecessaver

    del Hbonds[:]
    del Cbonds[:]

    grid.fill("")
    
    score = 0
    
    grid[6, 6] = protein[piecestart]
        
    x = 6
    y = 6
    
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
            grid[y, x] = protein[piecestart + i + 1]
        else:
            return -1
            
        if protein[piecestart + i + 1] == "H":
            giveHscore(directions[i], x, y)
        elif protein[piecestart + i + 1] == "C":
            giveHscore(directions[i], x, y)
            giveCscore(directions[i], x, y)
            
    score = len(Hbonds) + 5 * len(Cbonds)
    
    if bestproteins[0]['score'] == score:
        bfpiecessaver.append([piecestart, deepcopy(directions)])
        
    elif bestproteins[0]['score'] < score:
        del bestproteins[:]
        del bfpiecessaver[:]
        bestproteins.append({'score': score})
        bfpiecessaver.append([piecestart, deepcopy(directions)])
            
    return score

def hcproteinchecker():

    global bestproteins

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
                if Ccount > 0.:
                    print "Cprune: %f" %(len(Cbonds)*5/(Ccount-Cprune1))
                print "Hprune: %f" %(len(Hbonds)/(Hcount-Hprune1))
                printprotein(bestproteins[-1])

        elif bestproteins[0]['score'] < score:
            del bestproteins[:]
            bestproteins.append({'score': score, 'coordinates': deepcopy(coordinates), 'hbonds': deepcopy(Hbonds), 'cbonds': deepcopy(Cbonds)})
            elapsed_time = time.time() - start_time
            print "elapsed time: %f seconds" %elapsed_time
            if Ccount > 0.:
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
    