from venv import create
import numpy as np
import sys
import random
import params
import pandas as pd
import math
from random import random
import matplotlib.pyplot as plt

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
            magx = np.random.uniform(-10, 10)
            magy = np.random.uniform(-10, 10) 
            magz = np.random.uniform(-1, 1)

            spin = [magx, magy, magz]    
            spin[0] = magx / np.sqrt(magx**2 + magy**2 + magz**2)
            spin[1] = magy / np.sqrt(magx**2 + magy**2 + magz**2)
            spin[2] = magz / np.sqrt(magx**2 + magy**2 + magz**2)

            spinLattice[i][j] = spin

    return spinLattice


def chooseDeffects():
    if (params.deffects != False):
        spins = readDeffects(params.deffects)
    else:
        spins = createDeffectsAsArray()
    
    return spins 

def createDeffectsAsArray():
    if (params.deffects == False):
        return np.ones((params.Nx,params.Ny,3), np.float64)
    
    spinLattice = np.zeros((params.Nx,params.Ny,3), np.float64)
    
    for i in range(params.Nx):
        for j in range(params.Ny):
            
            spin = [1, 1, 1]    
            
            if (np.random.uniform(-1, 50) < 0 ):
                spin = [0,0,0]
           

            spinLattice[i][j] = spin

    return spinLattice

def createDeffectsAsFile():
    if (params.pinningDensity == 0):
        return np.ones((params.Nx,params.Ny,3))
    
    spinLattice = np.zeros((params.Nx,params.Ny), np.int0)
    totalPinnings = round(params.pinningDensity * params.spinsTotal/100);
    pinnings = 0;
    
    print("Number of pinnings: ", totalPinnings)
    
    while(pinnings < totalPinnings):
        if (np.random.uniform(1, 10) < 5 ):
            irand = np.random.randint(1,40)
            jrand = np.random.randint(1,40)
            spinLattice[irand][jrand] = 1
            pinnings = pinnings + 1

    np.savetxt(
        "output/vac_" + str(totalPinnings) + ".in", 
        spinLattice.reshape((params.spinsNumber, params.spinsNumber)), 
        fmt="%s", 
        delimiter='\t'
    )
    
    return 1

def createPBC(i, j):
    x1 = i - 1
    x2 = i + 1
    y1 = j - 1
    y2 = j + 1

    if (x1 < 0): x1 = params.Nx - 1
    if (x2 >= params.Nx): x2 = 0
    if (y1 < 0): y1 = params.Ny - 1
    if (y2 >= params.Ny): y2 = 0

    return x1,x2,y1,y2

def normalization(spins, deffects):
    for i in range(params.Nx):
        for j in range(params.Ny):
            spin = spins[i][j]
            pinning = deffects[i][j]

            if (pinning[0] == 1): spin = [0,0,0]
            
            magx = spin[0]
            magy = spin[1]
            magz = spin[2]

            denominator = np.sqrt(magx**2 + magy**2 + magz**2)

            if (denominator != 0):
                spin[0] = magx / denominator
                spin[1] = magy / denominator
                spin[2] = magz / denominator

            spins[i][j] = np.copy(spin)

    return spins

def iniRand(magphys):
    for i in range(params.Nx):
        for j in range(params.Ny):
            magx = np.np.random.uniform(-1, 1)
            magy = np.np.random.uniform(-1, 1) 
            magz = np.np.random.uniform(-1, 1)
            
            spin = [magx, magy, magz]

            magphys[i][j] = spin
    return magphys

def iniUniform():
    spins = np.ones((params.Nx,params.Ny,3), np.float64)
    return spins


#skyrmion
i0=int(params.Nx/2)
j0=int(params.Ny/2)
irange = np.arange(params.Nx)
jrange = np.arange(params.Ny)
r0 = 5 #radius

def prof(r):
    return (r/r0)*np.exp(-(r-r0)/r0)

def iniSkyrmionMicroLLG():
    xT, yT = np.meshgrid(irange-i0, jrange-j0)
    x=xT.T
    y=yT.T
    r=np.sqrt(x*x+y*y)+1.e-5
    
    magphys = np.ones((params.Nx,params.Ny,3), np.float64)
    magphys[:,:,0] = -prof(r)*x/r
    magphys[:,:,1] = prof(r)*y/r
    magphys[:,:,2] = np.sqrt(1.-magphys[:,:,0]*magphys[:,:,0]-magphys[:,:,1]*magphys[:,:,1])
    inds=np.where(r<r0)
    magphys[inds[0],inds[1],2] = -magphys[inds[0],inds[1],2]

    return magphys

def iniSkyrmionMumax():
    i0=int(params.Nx/2)
    j0=int(params.Ny/2)
    irange = np.arange(params.Nx)
    jrange = np.arange(params.Ny)

    x, y = np.meshgrid(irange-i0, jrange-j0)
    r=np.sqrt(x*x+y*y)+1.e-5
    
    p = -1 #polarization
    q = 1 #charge
    r2 = r * r
    
    magphys = np.ones((params.Nx,params.Ny,3), np.float64)
    
    magphys[:,:,2] =  2.0 *p * (np.exp(-r2 / (r0 * r0)) - 0.5)

    inds=np.where(r>0)
    magphys[inds[0],inds[1],1] = x[inds[0],inds[1]] * q / r[inds[0],inds[1]] * (1.0 - np.abs(magphys[inds[0],inds[1],2]))
    magphys[inds[0],inds[1],0] = -y[inds[0],inds[1]] * q / r[inds[0],inds[1]] * (1.0 - np.abs(magphys[inds[0],inds[1],2]))
    
    return magphys

## end skyrmion

#@todo: fix this, because is not a ferromagnetic
def iniFerromagnetic():
    return np.zeros((params.Nx, params.Ny,3), np.float64)

def iniVortex(spins):
    coords = np.linspace(-1, 1, 11)
    X, Y = np.meshgrid(coords, coords)
    Vx, Vy = Y, -X
    plt.figure()
    plt.quiver(X, Y, Vx, Vy, pivot='mid')
    plt.axis('square')
    plt.show()

    return spins

def kick(lattice, T):
    for i in range(params.Nx):
        for j in range(params.Ny):
            lattice[i,j][0] = np.copy(lattice[i,j][0]) + math.sqrt(T)*(2.0 * random() - 1.0)
            lattice[i,j][1] = np.copy(lattice[i,j][1]) + math.sqrt(T)*(2.0 * random() - 1.0) 
            lattice[i,j][2] = np.copy(lattice[i,j][2]) + math.sqrt(T)*(2.0 * random() - 1.0)

            magx = lattice[i,j][0]
            magy = lattice[i,j][1]
            magz = lattice[i,j][2]

            lattice[i,j][0] = magx / np.sqrt(magx**2.0 + magy**2.0 + magz**2.0)
            lattice[i,j][1] = magy / np.sqrt(magx**2.0 + magy**2.0 + magz**2.0)
            lattice[i,j][2] = magz / np.sqrt(magx**2.0 + magy**2.0 + magz**2.0)

    return lattice

def writeSpinLattice(spins, path, formatWith):
    spinsLattice = np.zeros((params.Nx,params.Ny,3), formatWith)
    aux = 0
    
    for x in range(params.Nx - 1, -1, -1):
        spinsLattice[aux] = spins[x]
        aux = aux + 1
    
    np.savetxt(path, spinsLattice.reshape((params.spinsNumber, 3 * params.spinsNumber)), fmt="%s", delimiter='\t')

def readSpinLattice(path):
    spins = pd.read_table(path, header=None)
    lines = len(spins)
    columns = len(spins.T)
    spinsLattice = np.zeros((params.Nx,params.Ny,3), np.float64)

    for x in range(lines -1, -1, -1):
        for j in range(0, columns, 3):
            spin = [spins[j][x],spins[j+1][x],spins[j+2][x]]
            spinsLattice[lines-1-x][int(j/3)] = spin
            
    return spinsLattice

def readDeffects(path):
    pinnings = pd.read_table(path, header=None)
    lines = len(pinnings)
    columns = len(pinnings)
    spinsLattice = np.zeros((params.Nx,params.Ny,3), np.float64)

    for i in range(lines):
        for j in range(columns):
            pinning = [1, 1, 1] 

            if (pinnings[i][j] == 1):
                pinning = [0,0,0]
            
            spinsLattice[j][i] = pinning
        
    
    return spinsLattice