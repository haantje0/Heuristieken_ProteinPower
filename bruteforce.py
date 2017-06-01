import time
import helpers as hps
import globalvariables as globalvars

def bruteforce():
    start_time = time.time()
    
    hps.setprotein()
    
    hps.setprune()
    
    bruteforcer(0)    
    
    elapsed_time = time.time() - start_time
    
    print "Your best score has a score of %i" %globalvars.bestproteins[0]['score']
    
    print "There are %i proteins with this score" %len(globalvars.bestproteins)
    
    print "Elapsed time: %f seconds" %elapsed_time

def bruteforcer(n):
    if n < (globalvars.lenprotein - 1): 
        globalvars.directions.append(0)
        if n > 0:
            for i in range(4):
   
                if globalvars.directions[n] != 3:
                    if hps.bfproteinchecker() < 0:
                        globalvars.directions[n] += 1
                    else:
                        bruteforcer(n + 1)
                        globalvars.directions[n] += 1 
                   
                else:
                    if hps.bfproteinchecker() < 0:
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
                    if hps.hcpieceproteinchecker() < 0:
                        globalvars.directions[n - globalvars.piecestart] += 1
                    else:
                        hcbruteforcer(n + 1)
                        globalvars.directions[n - globalvars.piecestart] += 1 
                   
                else:
                    if hps.hcpieceproteinchecker() < 0:
                        globalvars.directions.pop()
                        return 
                    else:                
                        hcbruteforcer(n + 1) 
                        globalvars.directions.pop()
        else:
            hcbruteforcer(n + 1)

    return