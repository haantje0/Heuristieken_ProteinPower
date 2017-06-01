import time
import helpers as hps
import globalvariables as globalvars
from random import randint
from copy import deepcopy
import bruteforce as bf

def hillclimber():    
    hps.setprotein()
    
    hillclimbslicer()
    
    hps.settimer()
            
    hillclimbing()
    
    elapsed_time = time.time() - globalvars.start_time
    
    hps.plotter()
    
    print "Your best score has a score of %i" %globalvars.bestproteins[0]['score']
    
    print "There are %i proteins with this score" %len(globalvars.bestproteins)
    
    print "it took %i times" %globalvars.counter
    
    print "Elapsed time: %f seconds" %elapsed_time

def hillclimbslicer():
        
    for i in range(len(globalvars.protein) - 5):
        globalvars.piecestart = i
        globalvars.pieceend = i + 5
        bf.hcbruteforcer(i)
                
        if globalvars.bfpiecessaver[0][2] >= 2:
            for j in globalvars.bfpiecessaver:
                globalvars.bfpieces.append(j)

        del globalvars.bfpiecessaver[:]
        globalvars.bfpiecessaver = [[0, [0,0,0,0,0], 0]]
    
    globalvars.piecestart = 0
    globalvars.pieceend = 0

            
def hillclimbing():

    while (time.time() - globalvars.start_time) < globalvars.timer:
        
        hps.setdirections()
        
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

                    for i in range(len(newdirectionpiece[1])):
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
        
            globalvars.score = hps.hcproteinchecker()
        
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