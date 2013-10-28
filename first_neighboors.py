#Neighbours's first rule beta


import numpy as np

#Hexagonos
s0='101001'
s1='010011'
s2='100110'
s3='001101'
s4='011010'
s5='110100'

#Hexagono vecino rotado en k*(pi/3)
R=0
#Hexagono central rotado en k*(pi/3)
C=0

#(til[V[i+1][j+1]])[4:6]+(til[V[i+1][j+1]][0:4])
#dic={'101001', '010011', '100110', '001101', '011010', '110100'}

til=[s0, s1, s2, s3, s4, s5]
#Ventana
V=np.array(([1, 3, 4],[3, 0, 1],[3, 4, 0]))
#Hexagono central
Center=til[V[1][1]]

#til[V[1][1]]
#Diferencia causada por los missed match
dE = 0

# Esta funcion entrega, dado el label de un hexagono
# la codificacion del hexagono como string
# ademas permite rotar el hexago por un multiplo
# n de n_alpha
def tile (label, n_alpha):
    tile = til[abs(label) - 1]
    return tile[n_alpha:] + tile[0:n_alpha]

def arista_dE (R, C):
    return 1 if R[3] != C[0] else 0

def dE_window (V):
    S = [[0,2],[0,1],[1,0],[2,0],[2,1],[1,2]]
    rot = [5, 4, 3, 2, 1, 0]
    dE = 0

    for i, vecino in enumerate(S):
        R = tile(V[vecino[0]][vecino[1]], rot[i])
        C = tile(V[1][1], rot[i])
        dE += arista_dE(R,C)
    return dE


V=np.array(([1, 3, 4],[3, 0, 1],[3, 4, 0]))



#for i in [-1, 0, 1]:
#    for j in [-1 ,0, 1]:
#        if (i+1 != j+1):
#            if (i+1 != 1 or j+1 != 2):
#               if (i+1 == 0) and (j+1 == 2):
#                   R = tile(V[0][2],5)
#                   C = tile(V[1][1],5)
#                   dE += arista_dE (R,C)
#               elif (i+1 == 0) and (j+1 == 1):
#                    R = tile(V[0][1],4)
#                    C = tile(V[1][1],4)
#                    dE += arista_dE (R,C)
#               elif (i+1 == 1) and (j+1 == 0):
#                    R = tile(V[1][0],3)
#                    C = tile(V[1][1],3)
#                    dE += arista_dE (R,C)
#               elif (i+1 == 2) and (j+1 == 0):
#                    R = tile(V[2][0],2)
#                    C = tile(V[1][1],2)
#                    dE += arista_dE (R,C)
#               elif (i+1 == 2) and (j+1 == 1):
#                    R = tile(V[2][1],1)
#                    C = tile(V[1][1],1)
#                    dE += arista_dE (R,C)
#            else:
#                R = til[V[1][2]]
#                C = Center
#                dE += arista_dE (R,C) 
#print("dE primer caso")
#print(dE)



