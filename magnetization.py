from typing import Final, final
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

            spin = [magx, magy, magz]

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
magdata=np.empty((Nframes,Nx+2,Ny+2,3),dtype=np.longdouble)
magdata[0]=np.copy(mag)

#main
spinPositions = lattice.createSpinPositions()
spins = magdata[0]

finalSpins = np.zeros((params.Nx + 2,params.Ny + 2,3), np.float64)
mag2 = np.zeros((Nx+2,Ny+2,3),np.float64)
magphys2 = mag[1:Nx+1,1:Ny+1,:]

spins = np.copy(lattice.normalization(spins))

for step in range(n):
    spins = np.copy(lattice.createPbc(spins))
    spins = np.copy(calc.llgEvolve(spins, finalSpins))
    spins = np.copy(lattice.normalization(spins))        

spins = np.copy(lattice.createPbc(spins))

plot.spins2D(spins)
