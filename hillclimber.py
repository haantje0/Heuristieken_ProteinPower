import time
import helpers as hps

start_time = time.time()

timer = 0
protein = 0

hps.settimer()

hps.setprotein()

hps.hillclimber()

elapsed_time = time.time() - start_time

hps.plotter()

print "Your best score has a score of %i" %hps.bestproteins[0]['score']

print "There are %i proteins with this score" %len(hps.bestproteins)

print "it took %i times" %hps.counter

print "Elapsed time: %f seconds" %elapsed_time
