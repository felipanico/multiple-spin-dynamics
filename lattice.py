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
    spinLattice = np.zeros((params.Nx+2,params.Ny+2,3), np.float64)
    
    for x in range(params.Nx):
        for y in range(params.Ny):
            magx = random.uniform(-10, 10)
            magy = random.uniform(-10, 10) 
            magz = random.uniform(1, 2)

            spin = [magx, magy, magz]

            spin[0] = magx / np.sqrt(magx**2 + magy**2 + magz**2)
            spin[1] = magy / np.sqrt(magx**2 + magy**2 + magz**2)
            spin[2] = magz / np.sqrt(magx**2 + magy**2 + magz**2)

            spinLattice[x][y] = spin
    
    return spinLattice

#a.T = transposed matrix of a
def createSkyrmion(Nx,Ny):
    spinLattice = np.zeros((Nx+2,Ny+2,3),np.float64)[1:Nx+1,1:Ny+1,:]
    normalization = (10)**(-3)

    i0=int(Nx/2)
    j0=int(Ny/2)
    
    irange = np.arange(Nx)
    jrange = np.arange(Ny)

    xT, yT = np.meshgrid(irange-i0, jrange-j0)
    x = xT.T
    y = yT.T

    r=np.sqrt(x*x+y*y)+1.e-5
    r0=10.

    spinLattice[:,:,0] = x*normalization
    spinLattice[:,:,1] = y*normalization
    spinLattice[:,:,2] = np.sqrt(1.-spinLattice[:,:,0]*spinLattice[:,:,0]-spinLattice[:,:,1]*spinLattice[:,:,1])
    inds=np.where(r<r0)
    spinLattice[inds[0],inds[1],2] = -spinLattice[inds[0],inds[1],2]       

    return spinLattice

#used by createSkyrmion
def prof(r, r0, x, y):
    return (r/r0)*np.exp(-(r-r0)/r0)
