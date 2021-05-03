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
    
    for x in range(params.Nx):
        for y in range(params.Ny):
            magx = random.uniform(-10, 10)
            magy = random.uniform(-10, 10) 
            magz = random.uniform(-1, 1)

            spin = [magx, magy, magz]

            spin[0] = magx / np.sqrt(magx**2 + magy**2 + magz**2)
            spin[1] = magy / np.sqrt(magx**2 + magy**2 + magz**2)
            spin[2] = magz / np.sqrt(magx**2 + magy**2 + magz**2)

            spinLattice[x][y] = spin

    return spinLattice

#Periodic Boundary Condtions
def createPbc(x,y):
    lineDown = x-1
    line = x
    lineUp = x+1

    columnRight = y+1
    column = y
    columnLeft = y-1

    if (lineDown <= 0):
        lineDown = params.Nx -1

    if (lineDown >= params.Nx):
        lineDown = 0

    if (lineUp <= 0):
        lineUp = params.Nx - 1 

    if (lineUp >= params.Nx):
        lineUp = 0

    if (columnLeft >= params.Ny ):
        columnLeft = 0

    if (columnLeft <= 0 ):
        columnLeft = params.Ny - 1				    		

    if (columnRight >= params.Ny):
        columnRight = 0

    if (columnRight <= 0):
        columnRight = params.Ny - 1

    return lineDown, line, lineUp, columnLeft, column, columnRight
