import numpy as np
import sys
import plot
import lattice
import calc
import params

# Parameters
n = params.n
h = params.h
Nx = params.Nx
Ny = params.Ny

# Create initial values and running calculation
mx = np.zeros((Nx*Ny,n-1))
my = np.zeros((Nx*Ny,n-1))
mz = np.zeros((Nx*Ny,n-1))

initialSpins = lattice.createSpinLattice()
spinPositions = lattice.createSpinPositions()
plot.spins2D(initialSpins, spinPositions)

finalSpins = np.zeros((params.Nx,params.Ny,3), np.float64)
for stepIndex in range(n-1):
	spinIndex = 0
	for x in range(Nx):
		for y in range(Ny):
			spin = calc.euler(initialSpins, x, y)
			initialSpins[x][y] = spin #finalSpins
			
			mx[spinIndex][stepIndex] = spin[0]
			my[spinIndex][stepIndex] = spin[1]
			mz[spinIndex][stepIndex] = spin[2]
			spinIndex = spinIndex + 1

plot.spins2D(initialSpins, spinPositions)
