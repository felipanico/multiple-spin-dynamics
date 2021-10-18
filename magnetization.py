import numpy as np
import sys
import plot
import lattice
import calc
import params
import monte_carlo

# Parameters
n = params.n
h = params.h
Nx = params.Nx
Ny = params.Ny

np.random.seed(0)
'''
# Create initial values and running calculation
mx = np.zeros((Nx*Ny,n-1))
my = np.zeros((Nx*Ny,n-1))
mz = np.zeros((Nx*Ny,n-1))

# Lattice from microLLG

mag = np.zeros((Nx+2,Ny+2,3)) ### including virtual nodes
magphys = mag[1:Nx+1,1:Ny+1,:] ### physical nodes
magphys = lattice.iniRand(magphys)

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

#main
spinPositions = lattice.createSpinPositions()
spins = magdata[0]

finalSpins = np.zeros((params.Nx + 2,params.Ny + 2,3))
mag2 = np.zeros((Nx+2,Ny+2,3))
magphys2 = mag[1:Nx+1,1:Ny+1,:]

spins = np.copy(lattice.normalization(spins))
'''

spins = lattice.createSpinLattice()
#print(spins)
#plot.spins2D(spins)

if (params.minimize):
    spins = np.copy(monte_carlo.metropolis(spins))
else:    
    for step in range(n):
        spins = np.copy(lattice.createPbc(spins))
        spins = np.copy(calc.llgEvolve(spins, finalSpins))
        spins = np.copy(lattice.normalization(spins))        

    spins = np.copy(lattice.createPbc(spins))

#print(spins)
plot.spins2DT(spins)
