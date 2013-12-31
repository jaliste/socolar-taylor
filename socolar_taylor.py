# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import numpy as np
import getopt,sys
import time
import math
try:
    import pygame
    import pygame.surfarray as surfarray
except ImportError:
    raise ImportError, "Numpy and Pygame required."


def Initialize (nSites):
    FORM = np.random.randint(0,11, (nSites,nSites))
    TRANS = np.array(range(-6,0) + range(1,7) )

    return (TRANS[FORM])


def moduler (K,N):
    return np.array(range(K-2,K+3)) % N


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
        
    return E / 2


zoom_factor = 4.0
gen_b = 100 *  np.array([1,0])
gen_a = 100 *  np.array([math.cos(math.pi/3), math.sin(math.pi/3)])


def ColorCell(cell, i, j):
   pos = zoom_factor * (np.array([0,0]) + i*gen_a + j*gen_b)
   surf = pygame.transform.rotozoom(hexagones[cell], 0, zoom_factor)
   screen.blit(surf, pos)
 
# Get command line arguments, if any
Tiles = np.array(range(-6,0) + range(1,7) )

#opts,args = getopt.getopt(sys.argv[1:],'t:n:c:s:')
#for key,val in opts:
#    if key == '-t': T        = int(val)
#    if key == '-n': nSites   = int(val)
#    if key == '-c': CellSize = int(val)
#    if key == '-s': nSteps   = int(val)

#print 'T = ', T
#print 'nSites = ', nSites
#print 'CellSize = ', CellSize
#print 'nSteps = ',nSteps
#print 'Initial Global Energy = ',global_E(nSites,lattice)


def subLattice(X, nSites):
    return np.bmat([[X]*nSites]*nSites) == 1
    

def paintLattice(Lattice):
    for i in range(nSites):
        for j in range(nSites):
            ColorCell(Lattice[i][j],i,j)
    pygame.display.flip()


def N_tau(tau):
    return 12000


def init_screen(size):
    pygame.init()
    UpColor = 255, 255, 255       # red
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('2D Socolar-Taylor Model Simulator')
    screen.fill(UpColor)
    pygame.display.flip()
    return screen
    

t_total = time.clock()

# Get display surface

# Clear display

# Create RGB array whose elements refer to screen pixels
#sptmdiag = surfarray.pixels3d(screen)

A = np.mat('1 0; 0 0')
B = np.mat('0 1; 0 0')
C = np.mat('0 0; 1 0')
D = np.mat('0 0; 0 1')

e_A = np.array([ math.sqrt(2/3.), 0,-1/math.sqrt(3)])
e_B = np.array([-math.sqrt(2/3.), 0,-1/math.sqrt(3)])
e_C = np.array([ 0, math.sqrt(2/3.), 1/math.sqrt(3)])
e_D = np.array([ 0,-math.sqrt(2/3.), 1/math.sqrt(3)])


# Set defaults
T = 1.0  # Temperature  
nSites = 32  #30
CellSize = 64  #16
zoom_factor = 7.0/nSites
hexagones = dict()
for idx in range(-6,0) + range(1,7):
    hexagones[idx] = pygame.image.load('hex' + str(idx) + '.png')

#-----------------------------------------------------

lattice = Initialize (nSites)
size = [int(e) for e in (gen_a+gen_b) * (nSites + 1) * zoom_factor]

spin_A = { 0: e_C, 1: e_B, 2: e_D }
spin_B = { 0: e_D, 1: e_A, 2: e_C }
spin_C = { 0: e_A, 1: e_D, 2: e_B }
spin_D = { 0: e_B, 1: e_C, 2: e_A } 
spins = [spin_A, spin_B, spin_C, spin_D]

def spin (tile_type, tile):
    #tile_type = 0 - > A, 1 -> B, 2 -> C, 3 -> D

    eq_tile = abs(tile) % 3
    return 3/2. * spins[tile_type][eq_tile]


def phi_1 (lattice, nSites):
    sublat = [
         subLattice(A,nSites/2) == 1,
         subLattice(B,nSites/2) == 1,
         subLattice(C,nSites/2) == 1,
         subLattice(D,nSites/2) == 1]
    N  = nSites * nSites
    sigma_n_tot = 1./N * sum([ sum([ spin (i, tile) for tile in lattice[sublat[i]]]) for i in [0,1,2,3]])

    return max([np.dot (sigma_n_tot, e) for e in [e_A,e_B,e_C,e_D]]) 

    


screen = init_screen(size)

# Main loop
def run():
    global T
    global lattice

    nSteps = 1000
    dT = 0.01
    t = 0
    t0 = time.clock()
    step = 0
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
        dE = dU(i,j,q_0,lattice)

        # flip if system will have lower energy
        if dE <= 0.:
            lattice[i][j] = q_0

            # otherwise do random decision     
        elif T > 0.0 and np.random.uniform() < math.exp(-dE/T):
            lattice[i][j] = q_0


        t += 1
        if (t % nSteps) == 0:
            paintLattice(lattice)
            t1 = time.clock()
            if (t1-t0) > 0.001:
                print 'Global Energy = ', global_E(nSites,lattice)
                print 'Phi_1 = ', phi_1(lattice, nSites)
                t0 = t1
                # calculate execution time
                dt = time.clock()-t_total

          #if T < 0.01: 
             #flag = -1
          #   print 'Initial Global Energy = ',IE   
          #   print 'Final Global Energy = ',global_E(nSites,lattice) 
          #   if global_E(nSites,lattice)==0:
          #       flag = -1
        step += 1
        if step >= N_tau(1):
            T -= dT
            if T < 0:
                T = 0.0
            else:
                print  "Temperatrure:", T
            step = 0

if __name__ == "__main__":
    run()
