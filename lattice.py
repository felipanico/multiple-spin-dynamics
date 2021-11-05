import numpy as np
import sys
import random
import params
import pandas as pd
import math
from random import random

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

#Periodic Boundary Condtions (microLLG based)
def createPbcTest(mag):
    aux = 1
    for i in range(params.Nx):
        mag[aux][0] = mag[aux][params.Ny]
        mag[aux][params.Ny + 1] = mag[aux][1]
        aux = aux + 1

    aux = 1
    for j in range(params.Ny):
        mag[0][aux] = mag[params.Nx][aux]
        mag[params.Nx + 1][aux] = mag[1][aux]
        aux = aux + 1    
    
    return mag

def normalization(spins):
    for i in range(params.Nx):
        for j in range(params.Ny):
            spin = spins[i][j]
            
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



i0=int(params.Nx/2)
j0=int(params.Ny/2)
irange = np.arange(params.Nx)
jrange = np.arange(params.Ny)

xT, yT = np.meshgrid(irange-i0, jrange-j0)
x=xT.T
y=yT.T
r=np.sqrt(x*x+y*y)+1.e-5

r0=10.
def prof(r):
	return (r/r0)*np.exp(-(r-r0)/r0)

def create_skyrmion(spins):
    spins[:,:,0] = -prof(r)*x/r
    spins[:,:,1] = -prof(r)*y/r
    spins[:,:,2] = np.sqrt(1.-spins[:,:,0]*spins[:,:,0]-spins[:,:,1]*spins[:,:,1])
    inds=np.where(r<r0)
    spins[inds[0],inds[1],2] = -spins[inds[0],inds[1],2]

    return spins

def skyrmion(spins):
    for i in range(params.Nx):
        for j in range(params.Ny):
            spin = spins[i][j]
            
            magx, magy, magz = spin[0]/1e-9-50, spin[1]/1e-9-50, spin[2]/1e-9

            if (spin[0] > 0 and spin[1] > 0 and spin[2] > 0):
                spin[0] = magx / np.sqrt(magx**2 + magy**2 + magz**2)
                spin[1] = magy / np.sqrt(magx**2 + magy**2 + magz**2)
                spin[2] = magz / np.sqrt(magx**2 + magy**2 + magz**2)

            spins[i][j] = np.array([-spin[1], spin[0], 10])

    return spins

"""
def arrayNormalize(v):
    normalized = np.array([0,0,0],  np.longdouble)
	
	magx = v[0]
	magy = v[1]
	magz = v[2]

	if (v[0] != 0 and v[1] != 0 and v[2] != 0):
		normalized[0] = magx / np.sqrt(magx**2 + magy**2 + magz**2)
		normalized[1] = magy / np.sqrt(magx**2 + magy**2 + magz**2)
		normalized[2] = magz / np.sqrt(magx**2 + magy**2 + magz**2)

	return normalized

"""
