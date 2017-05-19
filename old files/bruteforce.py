import time
import numpy as np
from copy import deepcopy
import bruteforcehelpers as bhps

start_time = time.time()

bhps.placer()

bhps.proteinplacer()

bhps.bruteforcer(len(bhps.directions) - 1)

bhps.plotter()

print "there are %i proteins with this score" %len(bhps.bestproteins)

elapsed_time = time.time() - start_time

print "elapsed time: %f seconds" %elapsed_time
