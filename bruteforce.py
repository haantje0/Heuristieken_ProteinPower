import time
import helpers as hps

start_time = time.time()

hps.setprotein("HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH")

hps.setprune(5.0, 0.75, 2.0, 3.75)

hps.bruteforcer(0)

elapsed_time = time.time() - start_time

print "Your best score has a score of %i" %hps.bestproteins[0]['score']

print "There are %i proteins with this score" %len(hps.bestproteins)

print "Elapsed time: %f seconds" %elapsed_time
