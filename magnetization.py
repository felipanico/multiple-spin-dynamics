from typing import final
import numpy as np
import sys
import plot
import lattice
import calc
import params
import random

# Parameters
n = params.n
h = params.h
Nx = params.Nx
Ny = params.Ny

# Create initial values and running calculation
mx = np.zeros((Nx*Ny,n-1))
my = np.zeros((Nx*Ny,n-1))
mz = np.zeros((Nx*Ny,n-1))

# test (microLLG)

def ini_rand2():
    for i in range(Nx):
        for j in range(Ny):
            magx = i + 1
            magy = j + 1
            magz = magx + magy

            #magx = random.uniform(-10, 10)
            #magy = random.uniform(-10, 10) 
            #magz = random.uniform(-1, 1)
            
            spin = [magx, magy, magz]

            #spin[0] = magx / np.sqrt(magx**2 + magy**2 + magz**2)
            #spin[1] = magy / np.sqrt(magx**2 + magy**2 + magz**2)
            #spin[2] = magz / np.sqrt(magx**2 + magy**2 + magz**2)

            magphys[i][j] = spin

mag = np.zeros((Nx+2,Ny+2,3),np.float64) ### including virtual nodes
magphys = mag[1:Nx+1,1:Ny+1,:] ### physical nodes
ini_rand2()

mag[0,1:Ny+1,:]=magphys[1,:,:]
mag[Nx+1,1:Ny+1,:]=magphys[Nx-1,:,:]

mag[0:Nx,0,:]=magphys[:,0,:]
mag[1:Nx+1,Ny+1,:]=magphys[:,Ny-1,:]

mag[0,0,:]=0.
mag[0,Ny+1,:]=0.
mag[Nx+1,0,:]=0.
mag[Nx+1,Ny+1,:]=0.


Nframes = 16
magdata=np.empty((Nframes,Nx+2,Ny+2,3),dtype=np.float64)
magdata[0]=np.copy(mag)

spinPositions = lattice.createSpinPositions()
initialSpins = magdata[0]

#plot.spins2D(initialSpins, spinPositions)

finalSpins = np.zeros((params.Nx,params.Ny,3), np.float64)
mag2 = np.zeros((Nx+2,Ny+2,3),np.float64)
magphys2 = mag[1:Nx+1,1:Ny+1,:]

for stepIndex in range(n):
    spinIndex = 0
    for x in range(Nx):
        for y in range(Ny):
            spin = calc.euler(initialSpins, x, y)
            finalSpins[x][y] = spin
            magphys2[x][y] = spin
            spinIndex = spinIndex + 1

for aux in range(Nx):
    mag2[aux+1][1] = finalSpins[aux]
    
print(mag2)

