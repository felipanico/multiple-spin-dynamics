from typing import final
from matplotlib import set_loglevel
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

spinPositions = lattice.createSpinPositions()
initialSpins = lattice.createSpinLattice()

plot.spins2D(initialSpins, spinPositions)
finalSpins = np.zeros((params.Nx,params.Ny,3), np.float64)

for stepIndex in range(n-1):
    spinIndex = 0
    for x in range(Nx):
        for y in range(Ny):
            spin = calc.euler(initialSpins, x, y)
            finalSpins[x][y] = spin
            mx[spinIndex] = spin[0]
            my[spinIndex] = spin[1]
            mz[spinIndex] = spin[2]
            spinIndex = spinIndex + 1

plot.spins2D(finalSpins, spinPositions)
#plot.spins3D(stepIndex, params.spinsTotal, mx,my,mz)
