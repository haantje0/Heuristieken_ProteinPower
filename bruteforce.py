import time
import helpers as hps
import globalvariables as globalvars

def bruteforce():
    start_time = time.time()
    
    hps.setprotein()
    
    hps.setprune()
    
    hps.bruteforcer(0)
    
    elapsed_time = time.time() - start_time
    
    print "Your best score has a score of %i" %globalvars.bestproteins[0]['score']
    
    print "There are %i proteins with this score" %len(globalvars.bestproteins)
    
    print "Elapsed time: %f seconds" %elapsed_time
