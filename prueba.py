import numpy as N
from random import randint
def Initialize(nSites):
	state = N.zeros((nSites,nSites))
	for i in range(nSites):
	   for j in range(nSites):
	      if randint(0,1) > 0.5:     # dipole spin up
	          state[i][j] = 1
	      else :  state[i][j] = 0	 # dipole spin down
	      
	return state


