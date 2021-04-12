import numpy as np
import sys
import plot
import lattice
import calc
import params

# Parameters for higher magnetic field
n = params.n
h = params.h
Nx = params.Nx
Ny = params.Ny

# Create initial values and running calculation
mx = np.zeros((Nx*Ny,n-1))
my = np.zeros((Nx*Ny,n-1))
mz = np.zeros((Nx*Ny,n-1))

spinLattice = lattice.createSpinLattice()
spinPositions = lattice.createSpinPositions()
plot.spins2D(spinLattice, spinPositions)

for stepIndex in range(n-1):
	spinIndex = 0
	for x in range(Nx):
		for y in range(Ny):
			spin = calc.euler(spinLattice[x][y], spinLattice, x, y)
			mx[spinIndex][stepIndex] = spin[0]
			my[spinIndex][stepIndex] = spin[1]
			mz[spinIndex][stepIndex] = spin[2]
			spinIndex = spinIndex + 1

plot.spins2D(spinLattice, spinPositions)
