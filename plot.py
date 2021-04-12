import numpy as np
from matplotlib import pyplot as plt
import random
import sys
import params

def individualMagnetization(mx, my, mz):
	plt.plot(mx, label = 'mx')
	plt.plot(my, label = 'my')
	plt.plot(mz, label = 'mz')
	plt.title('Magnetization')
	plt.show()

def spins2D(spinLattice, spinPositions):
	fig, ax = plt.subplots(figsize=(6,6))
	
	x = np.zeros(params.spinsTotal)
	y = np.zeros(params.spinsTotal)
	sx = np.zeros(params.spinsTotal)
	sy = np.zeros(params.spinsTotal)
	sz = np.zeros(params.spinsTotal)
	
	for k in range(params.spinsTotal):
		x[k] = spinPositions[k][0]
		y[k] = spinPositions[k][1]
		
	k = 0
	for i in range(params.Nx):
		for j in range(params.Ny):
			sx[k] = spinLattice[i][j][0]
			sy[k] = spinLattice[i][j][1]
			sz[k] = spinLattice[i][j][2]
			k = k + 1
    				
	sz = sz.reshape(params.spinsNumber, -1)
	
	ax.quiver(x, y, sx, sy, linewidth=5)
	im = ax.imshow(sz, cmap='bwr')
	fig.colorbar(im, ax=ax)

	plt.show()
	

#size - number of loops
#spinTotal - spin number of lattice
#mx, my, mz - magnetizations in x,y and z direction

def spins3D(size, spinTotal, mx, my, mz):
	fig3 = plt.figure()
	cx = fig3.gca(projection='3d')
	
	x = np.zeros(spinTotal)
	y = np.zeros(spinTotal)
	z = np.zeros(spinTotal)
	
	sx = np.zeros((spinTotal))
	sy = np.zeros((spinTotal))
	sz = np.zeros((spinTotal))

	for k in range(spinTotal):
		x[k] = random.uniform(1, 2)
		y[k] = random.uniform(1, 2)
		z[k] = random.uniform(1, 2)

		sx[k] = mx[k][size-1]
		sy[k] = my[k][size-1]
		sz[k] = mz[k][size-1]

	cx.quiver(x, y, z, sx, sy, sz, length=0.05, normalize=True)
	plt.show()