import numpy as np
import sys
import plot
import lattice
import calc

n = 2000
h = 0.05
Nx = 5
Ny = 5
H = np.array([0,0,1])

sx = []
sy = []
sz = []

mx = np.zeros((Nx*Ny,n-1))
my = np.zeros((Nx*Ny,n-1))
mz = np.zeros((Nx*Ny,n-1))

spinLattice = lattice.createSpinLattice(n,Nx,Ny,mx,my,mz)

spinTotal = Nx*Ny

plot.spins2D(spinLattice)

for t in range(n-1):
	i = 0
	for x in range(Nx):
		for y in range(Ny):
			spin = calc.euler(H, spinLattice, spinLattice[x][y], x, y, h)
			mx[i][t] = spin[0]
			my[i][t] = spin[1]
			mz[i][t] = spin[2]
			i = i+1

plot.spins2D(spinLattice)

