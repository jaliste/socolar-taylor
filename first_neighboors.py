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
Diff=0

for i in [-1, 0, 1]:
    for j in [-1 ,0, 1]:
        if (i+1!=j+1):
            if (i+1!=1 or j+1!=2):
               if (i+1==0) and (j+1==2):
                   R=(til[V[0][2]])[5:6]+(til[V[0][2]][0:5])
                   C=(til[V[1][1]])[5:6]+(til[V[1][1]][0:5])
                   if R[3]!=C[0]:
                       Diff=Diff+1
               elif (i+1==0) and (j+1==1):
                    R=(til[V[0][1]])[4:6]+(til[V[0][1]][0:4])
                    C=(til[V[1][1]])[4:6]+(til[V[1][1]][0:4])
                    if R[3]!=C[0]:
                       Diff=Diff+1
               elif (i+1==1) and (j+1==0):
                    R=(til[V[1][0]])[3:6]+(til[V[1][0]][0:3])
                    C=(til[V[1][1]])[3:6]+(til[V[1][1]][0:3])
                    if R[3]!=C[0]:
                       Diff=Diff+1
               elif (i+1==2) and (j+1==0):
                    R=(til[V[2][0]])[2:6]+(til[V[2][0]][0:2])
                    C=(til[V[1][1]])[2:6]+(til[V[1][1]][0:2])
                    if R[3]!=C[0]:
                       Diff=Diff+1
               elif (i+1==2) and (j+1==1):
                    R=(til[V[2][1]])[1:6]+(til[V[2][1]][0:1])
                    C=(til[V[1][1]])[1:6]+(til[V[1][1]][0:1])
                    if R[3]!=C[0]:
                       Diff=Diff+1
            else:
                if (til[V[1][2]])[3]!=Center[0]:
                    Diff=Diff+1
                 
        