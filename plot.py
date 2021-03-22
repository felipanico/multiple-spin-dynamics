import numpy as np
from matplotlib import pyplot as plt
import random
import sys

def individualMagnetization(mx, my, mz):
	plt.plot(mx, label = 'mx')
	plt.plot(my, label = 'my')
	plt.plot(mz, label = 'mz')
	plt.title('Magnetization')
	plt.show()

def spins2D(spinLattice, scale, zmin, zmax):
	fig, ax = plt.subplots(figsize=(6,6))
	cmap = plt.get_cmap('coolwarm_r')
	width = 0.0025
	interpolation='nearest'

	x = spinLattice[:,:,0]
	y = spinLattice[:,:,1]
	z = spinLattice[:,:,2]

	normalization = (10)**(-2)

	xNormalized = (x / np.sqrt(x**2 + y**2 + z**2))
	yNormalized = (y / np.sqrt(x**2 + y**2 + z**2))
	
	print('x')
	print(xNormalized)
	
	print('z')
	print(z)

	im=ax.imshow(z, interpolation=interpolation, cmap = cmap, origin='lower', vmin=zmin, vmax=zmax)
	ax.quiver(xNormalized, yNormalized, pivot='mid', zorder=2, width=width, scale=scale ,scale_units='xy', headwidth=6, headlength=8)
	fig.colorbar(im, label=r'$m_z$', orientation='vertical')
	
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