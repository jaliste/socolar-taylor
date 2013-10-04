#Phy250 Project: Ising Model Simulator  by Jim Ma
#
# TwoDIsing.py: Two-dimensional Ising Model simulator
# 	Using PyGame/SDL graphics
#
"""
 Options:
 -t #  Temperature
 -n #  Size of lattice
 -c #  Size of cell
 -s #  Number of time steps
"""

from numpy import *
from numpy.random import *
import getopt,sys
import time
from random import randint
try:
	import Numeric as N
	import pygame
	import pygame.surfarray as surfarray
except ImportError:
	raise ImportError, "Numeric and PyGame required."

#
#                 Ising Model routines                    #
#
# Initialize crystal lattice, load in initial configuration
def Initialize(nSites):
	state = N.zeros((nSites,nSites))
	for i in range(nSites):
	   for j in range(nSites):
	      if randint(0,1) > 0.5:     # dipole spin up
	          state[i][j] = 1
	      else :  state[i][j] = -1	 # dipole spin down
	      
	return state

# Use Mean Field approximation and periodic BC to compute 
# dU for decision to flip a dipole
#                
def dU(i, j, nSites, state):    
   m = nSites - 1 
   if i == 0 :                # state[0,j]
      top = state[m,j]
   else : 
      top = state[i-1,j]

   if i == m :                # state[m,j]
      bottom = state[0,j]
   else : 
      bottom = state[i+1,j]  

   if j == 0 :                # state[i,0]
      left = state[i,m]
   else : 
      left = state[i,j-1]

   if j == m :                # state[i,m]
      right = state[i,0]
   else : 
      right = state[i,j+1]  

   return 2.*state[i,j]*(top+bottom+left+right)

# Color the cell based on dipole direction:
#     Dipole spin is up : color cell red
#     Dipole spin is down : color cell blue 
#                
def ColorCell(state,i,j):
   if state[i][j] > 0:    # dipole spin is up
	  screen.fill(UpColor,[i*CellSize,j*CellSize,CellSize,CellSize])
   else : screen.fill(DownColor,[i*CellSize,j*CellSize,CellSize,CellSize])
  
# Set defaults
T = 2  # Temperature  
nSites   = 30 #30
CellSize = 24  #16
nSteps = 1000   
 

# Get command line arguments, if any
opts,args = getopt.getopt(sys.argv[1:],'t:n:c:s:')
for key,val in opts:
	if key == '-t': T        = int(val)
	if key == '-n': nSites   = int(val)
	if key == '-c': CellSize = int(val)
	if key == '-s': nSteps   = int(val)
	
print 'T = ', T
print 'nSites = ', nSites
print 'CellSize = ', CellSize
print 'nSteps = ',nSteps

size = (CellSize*nSites,CellSize*nSites)
	# Set initial configuration
state = Initialize(nSites)

pygame.init()
UpColor = 255, 0, 0       # red
DownColor = 0, 0, 255     # blue
	# Get display surface
screen = pygame.display.set_mode(size)
pygame.display.set_caption('2D Ising Model Simulator')
	# Clear display
screen.fill(UpColor)
pygame.display.flip()
	# Create RGB array whose elements refer to screen pixels
sptmdiag = surfarray.pixels3d(screen)

    # display initial dipole configuration
for i in range(nSites):
   for j in range(nSites):
      if state[i][j] < 0:
	    screen.fill(DownColor,[i*CellSize,j*CellSize,CellSize,CellSize])

t = 0
t0 = time.clock()
    # total execution time
t_total = time.clock()

# Main loop
flag = 1
while flag > 0:
	for event in pygame.event.get():
	    # Quit running simulation
		if event.type == pygame.QUIT: sys.exit()
		# randomly select cell 
        i = int(random(1)*nSites) 
       	j = int(random(1)*nSites)  
       	# Any system energy change if flip dipol
    	dE = dU(i,j,nSites,state)
    	# flip if system will have lower energy
    	if dE <= 0. :
           state[i][j] = -state[i][j]
           ColorCell(state, i, j)
        # otherwise do random decision     
        elif random(1) < exp(-dE/T) :
             state[i][j] = -state[i][j]
             ColorCell(state, i, j)
    
	pygame.display.flip()
	t += 1
	if (t % nSteps) == 0:
		t1 = time.clock()
		if (t1-t0) > 0.001 :
		   print 't1 = ', t1
		   print "Iterations per second: ", float(nSteps) / (t1 - t0)
		t0 = t1
	# calculate execution time
	dt = time.clock()-t_total
	if dt > 200.0 : flag = -1
#matshow(state)	
print "Total simulation time is %g seconds of temperature %g K" % (dt,T)
