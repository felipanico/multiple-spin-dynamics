import numpy as np
import sys
import random
import plot
import lattice
import calc

n = 1000
h = 0.05
Nx = 2
Ny = 2
H = np.array([0,0,1])
position = 1.0 / np.sqrt(3.0)

sx = []
sy = []
sz = []

mx = np.zeros((Nx*Ny,n-1))
my = np.zeros((Nx*Ny,n-1))
mz = np.zeros((Nx*Ny,n-1))

spinLattice = lattice.createSpinLattice(n,Nx,Ny,mx,my,mz)

spinTotal = Nx*Ny
xAxis = np.zeros((spinTotal))
yAxis = np.zeros((spinTotal))
zAxis = np.zeros((spinTotal))

for k in range(spinTotal):
	xAxis[k] = random.uniform(1, 2)
	yAxis[k] = random.uniform(1, 2)
	zAxis[k] = random.uniform(1, 2)

plot.positions3D(spinTotal, spinTotal, xAxis, yAxis, zAxis, mx, my, mz)

for t in range(n-1):
	i = 0
	for x in range(Nx):
		for y in range(Ny):
			spin = calc.euler(H, spinLattice, spinLattice[x][y], x, y, h)
			mx[i][t] = spin[0]
			my[i][t] = spin[1]
			mz[i][t] = spin[2]
			i = i+1

plot.positions3D(t, spinTotal, xAxis, yAxis, zAxis, mx, my, mz)

