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

spinLattice = lattice.createSpinLattice(n,Nx,Ny,mx,my,mz)
spinTotal = Nx*Ny

plot.spins2D(spinLattice, 0.1, 0.5)

for stepIndex in range(n-1):
	spinIndex = 0
	for x in range(Nx):
		for y in range(Ny):
			spin = calc.euler(spinLattice[x][y], spinLattice, stepIndex, x, y)
			mx[spinIndex][stepIndex] = spin[0]
			my[spinIndex][stepIndex] = spin[1]
			mz[spinIndex][stepIndex] = spin[2]
			spinIndex = spinIndex + 1

print(spinLattice)
plot.spins2D(spinLattice, -1, 1)
plot.spins3D(stepIndex, spinTotal, mx, my, mz)

