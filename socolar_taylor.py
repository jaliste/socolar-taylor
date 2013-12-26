# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import numpy as np
from numpy import *
from numpy.random import *
import getopt,sys
import time
from random import randint
try:
    
    import pygame
    import pygame.surfarray as surfarray
except ImportError:
    raise ImportError, "Numpy and Pygame required."

def Initialize (nSites):
    FORM = np.random.randint(0,11, (nSites,nSites))
    TRANS = array(range(-6,0) + range(1,7) )
    
    return (TRANS[FORM])

# Set defaults
T = 2.0  # Temperature  
nSites   = 8 #30
CellSize = 64  #16
nSteps = 1000
dT = 0.01
step = 0
#-----------------------------------------------------

Latice = Initialize (nSites)
Tiles = array(range(-6,0) + range(1,7) )

def moduler (K,N):
    return array(range(K-2,K+3)) % N

def Wmaker (M, i, j):
    L = M.shape

    return M[moduler(i,L[0])] [:, moduler(j,L[1])]

def tileFNR (label, n_alpha):
    #Hexagonos
    s1='101001'
    s2='010011'
    s3='100110'
    s4='001101'
    s5='011010'
    s6='110100'
    
    til=[s1, s2, s3, s4, s5, s6]
    
    tile = til[abs(label) - 1]
    return tile[n_alpha:] + tile[0:n_alpha]

def Match_Detector (R, C):
    return 0 if R[3] != C[0] else 1

def dE_FNRCalculator (V):
    S = [[2,3],[3,2],[3,1],[2,1],[1,2],[1,3]]
    rot = [0, 1, 2, 3, 4, 5]
    dE = 0

    for i, vecino in enumerate(S):
        R = tileFNR(V[vecino[0]][vecino[1]], rot[i])
        C = tileFNR(V[2][2], rot[i])
        dE += Match_Detector(R,C)
    return dE

def tileSNR (label, n_alpha):
    #Hexagonos
    F1='010011'
    F2='100110'
    F3='001101'
    F4='011010'
    F5='110100'
    F6='101001'

    #Hexagonos Volteados
    f1='011010'
    f2='110100'
    f3='101001'
    f4='010011'
    f5='100110'
    f6='001101'

    F=[F1, F2, F3, F4, F5, F6]
    f=[f1, f2, f3, f4, f5, f6]
    
    if (label)>0:
       tile = F[(abs(label))-1]
    else:
        tile = f[(abs(label))-1]
    return tile[n_alpha:] + tile[0:n_alpha]

def dE_SNRCalculator (V):
    S = [[1,4],[3,3],[4,1],[3,0],[1,1],[0,3]]
    rot= [0,1,2,3,4,5]
    dE = 0
    
    
    
    for i, vecino in enumerate(S):
        R = tileSNR(V[vecino[0]][vecino[1]], rot[i])
        C = tileSNR(V[2][2], rot[i])
        dE += Match_Detector(R,C)
    return dE


def Pre_dE (i,j,L):
    V = Wmaker(L, i, j)
    return dE_FNRCalculator(V) + dE_SNRCalculator (V)
    
def Post_dE(i,j,q_0,L):
    V = Wmaker(L, i, j)
    
    V[2][2]=q_0
    
    return dE_FNRCalculator(V) + dE_SNRCalculator (V)
    
def dU (i,j,q_0,L):
    
    return Post_dE(i,j,q_0,L) - Pre_dE (i,j,L)
    
def global_E(D,M):
    E = 0
    for i in range(D):
        for j in range(D):
            E += Pre_dE (i,j,M)
        
    return E

IE = global_E(nSites,Latice)    

zoom_factor = 10.0/nSites

gen_a = 50 *  np.array([math.cos(math.pi/6),math.sin(math.pi/6)])
gen_b = 50 *  np.array([math.cos(-math.pi/6),math.sin(-math.pi/6)])

def ColorCell(cell, i, j):
   pos = zoom_factor * (np.array([20,20]) + i*gen_a + j*gen_b)
   surf = pygame.transform.rotozoom(hexagones[cell], 0, zoom_factor)
   screen.blit(surf, pos)
 
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
print 'Initial Global Energy = ',global_E(nSites,Latice)
size = (int(CellSize*nSites*2*zoom_factor),int(CellSize*nSites*zoom_factor))

# Set initial configuration
state = Initialize(nSites)

pygame.init()
UpColor = 255, 0, 0       # red
DownColor = 0, 0, 255     # blue

# Get display surface
screen = pygame.display.set_mode(size)
pygame.display.set_caption('2D Socolar-Taylor Model Simulator')

# Clear display
screen.fill(UpColor)
pygame.display.flip()

# Create RGB array whose elements refer to screen pixels
#sptmdiag = surfarray.pixels3d(screen)
    
hexagones = dict()
for idx in range(-6,0) + range(1,7):
    hexagones[idx] = pygame.image.load('hex' + str(idx) + '.png')


#screen.blit (hexa_image, hexa)
# display initial dipole configuration
def paintLatice(Latice):
    for i in range(nSites):
        for j in range(nSites):
            ColorCell(Latice[i][j],i,j)

def N_tau(tau):
    return 120

#ColorCell(1,0,0)
#ColorCell(-1,0,1)
#ColorCell(-2,1,1)
#ColorCell(2,1,2)
#ColorCell(3,2,2)
#ColorCell(-3,2,3)
#ColorCell(4,3,3)
#ColorCell(-4,3,4)
#ColorCell(5,4,4)
#ColorCell(-5,4,5)
#ColorCell(6,5,5)
#ColorCell(-6,5,6)
#Vent  = Wmaker(Latice, 4,4)
#print "Energia primeros" + str(dE_FNRCalculator(Vent)) + " segundos:" + str( dE_SNRCalculator (Vent)) 
#print (dE_FNRCalculator(Vent) + dE_SNRCalculator(Vent))
#for i in range(-2,3):
#	for j in range (-2,3):
#		ColorCell(Vent[i][j], i + 5, j + 5)


paintLatice(Latice)
t = 0
t0 = time.clock()
    # total execution time
t_total = time.clock()

# Main loop
if __name__ == "__main__":
    flag = 1
    while flag > 0:

        for event in pygame.event.get():
        # Quit running simulation
            if event.type == pygame.QUIT: sys.exit()

        # randomly select cell 
        i = np.random.randint(0,nSites) 
        j = np.random.randint(0,nSites)
        q_0 = np.random.choice(Tiles)

        # Any system energy change if flip dipol
        dE = dU(i,j,q_0,Latice)

        # flip if system will have lower energy
        if dE <= 0.:
            Latice[i][j] = q_0
            ColorCell(Latice[i][j], i, j)

            # otherwise do random decision     
        elif random(1) < exp(-dE/T):
            Latice[i][j] = q_0
            ColorCell(Latice[i][j], i, j)


        pygame.display.flip()
        t += 1

        if (t % nSteps) == 0:
            t1 = time.clock()
            if (t1-t0) > 0.001:
                print 't1 = ', t1
                print "Iterations per second: ", float(nSteps) / (t1 - t0)
                print 'Global Energy = ',global_E(nSites,Latice)
                t0 = t1
                # calculate execution time
                dt = time.clock()-t_total

          #if T < 0.01: 
             #flag = -1
          #   print 'Initial Global Energy = ',IE   
          #   print 'Final Global Energy = ',global_E(nSites,Latice) 
          #   if global_E(nSites,Latice)==0:
          #       flag = -1
        step += 1
        if step >= N_tau(1) and T-dT > 0.0:
            T -= dT
            step = 0
            print "Temperature:", T

