import numpy as np
import sys
import random
import params
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

#Periodic Boundary Condtions
def createPbc(mag):
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
    for i in range(params.Nx + 1):
        for j in range(params.Ny + 1):
            spin = spins[i+1][j+1]
            
            magx = spin[0]
            magy = spin[1]
            magz = spin[2]

            if (spin[0] > 0 and spin[1] > 0 and spin[2] > 0):
                spin[0] = magx / np.sqrt(magx**2 + magy**2 + magz**2)
                spin[1] = magy / np.sqrt(magx**2 + magy**2 + magz**2)
                spin[2] = magz / np.sqrt(magx**2 + magy**2 + magz**2)

            spins[i+1][j+1] = np.copy(spin)

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

def sphericalRand():
    """
    Generate random unit vector in cartesian coordinates
    :return: [x, y, z] the unit vector
    """

    phi = np.np.random.uniform(0, 2 * np.pi)
    u = np.np.random.uniform(0, 1)
    theta = np.arccos(2 * u - 1)
    
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    
    return np.array([x, y, z])


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

def randomWithPBC():
    
    Nx = params.Nx
    Ny = params.Ny
    
    mag = np.zeros((Nx+2,Ny+2,3)) ### including virtual nodes
    magphys = mag[1:Nx+1,1:Ny+1,:] ### physical nodes
    magphys = iniRand(magphys)

    mag[0,1:Ny+1,:]=magphys[1,:,:]
    mag[Nx+1,1:Ny+1,:]=magphys[Nx-1,:,:]

    mag[0:Nx,0,:]=magphys[:,0,:]
    mag[1:Nx+1,Ny+1,:]=magphys[:,Ny-1,:]

    mag[0,0,:]=0.
    mag[0,Ny+1,:]=0.
    mag[Nx+1,0,:]=0.
    mag[Nx+1,Ny+1,:]=0.

    Nframes = 16
    magdata=np.empty((Nframes,Nx+2,Ny+2,3))
    magdata[0]=np.copy(mag)

    return magdata[0]