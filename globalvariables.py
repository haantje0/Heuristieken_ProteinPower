import time
import numpy as np

start_time = time.time()

protein = []

lenprotein = 0

Hprune1 = -1.
Hprune2 = -1.

Cprune1 = -1.
Cprune2 = -1.

grid = np.chararray(1, 1)

x = 0
y = 0

Hbonds = []
Cbonds = []

Hcount = 0
Ccount = 0

score = -1.

counter = 0
timer = 0

bfpiecessaver = [[0, [0,0,0,0,0], 0]]
bfpieces = [[0, [0,0,0,0,0], 0]]
piecestart = 0
pieceend = 0

directions = []

coordinates = [{'coordinate': ([0,0]),'letter': "P"}]

bestproteins = [{'score': score, 'coordinates': coordinates, 'hbonds': Hbonds, 'cbonds': Cbonds}]
