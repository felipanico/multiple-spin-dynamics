import numpy as np
import sys
import random
import params

def createSpinPositions():
    positions = np.zeros([params.spinsTotal, 3])
    x = 0
    y = 0
    
    for k in range(params.spinsTotal):
        positions[k] = [x, y , 0]
        x = x + 1

        if ((k+1) % params.spinsNumber == 0):
            y = y + 1
            x = 0
    
    return positions  

def createSpinLattice():
    spinLattice = np.zeros((params.Nx,params.Ny,3), np.float64)
    
    for i in range(params.Nx):
        for j in range(params.Ny):
            magx = random.uniform(-10, 10)
            magy = random.uniform(-10, 10) 
            magz = random.uniform(-1, 1)

            #magx = i + 1
            #magy = j + 1
            #magz = magx + magy

            spin = [magx, magy, magz]

            spin[0] = magx / np.sqrt(magx**2 + magy**2 + magz**2)
            spin[1] = magy / np.sqrt(magx**2 + magy**2 + magz**2)
            spin[2] = magz / np.sqrt(magx**2 + magy**2 + magz**2)

            spinLattice[i][j] = spin

    return spinLattice

#Periodic Boundary Condtions
def createPbc(mag):
    aux = 1
    for i in range(params.Nx):
        mag[aux][0] = mag[aux][1]
        mag[aux][params.Ny + 1] = mag[aux][params.Ny]
        aux = aux + 1

    aux = 1
    for j in range(params.Ny):
        mag[0][aux] = mag[params.Nx][aux]
        mag[params.Nx + 1][aux] = mag[1][aux]
        aux = aux + 1    
    
    return mag
