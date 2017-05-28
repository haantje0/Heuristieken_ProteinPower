import time
import helpers as hps
import globalvariables as globalvars

def hillclimber():
    print "JE BENT ER!"    
    
    hps.setprotein()
    
    hps.hillclimbslicer()
    
    hps.settimer()
    
    hps.hillclimber()
    
    elapsed_time = time.time() - globalvars.start_time
    
    hps.plotter()
    
    print "Your best score has a score of %i" %globalvars.bestproteins[0]['score']
    
    print "There are %i proteins with this score" %len(globalvars.bestproteins)
    
    print "it took %i times" %globalvars.counter
    
    print "Elapsed time: %f seconds" %elapsed_time
