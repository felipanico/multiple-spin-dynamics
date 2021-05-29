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


def spins2D(magdata):
	fig, ax = plt.subplots(figsize=(6,6))
	interpolation='nearest'
	cmap=plt.get_cmap('coolwarm_r')
	Nx = params.Nx
	Ny = params.Ny

	mx=magdata[1:Nx+1,1:Ny+1,0]
	my=magdata[1:Nx+1,1:Ny+1,1]
	mz=magdata[1:Nx+1,1:Ny+1,2]
	
	im=ax.imshow(mz.T,interpolation=interpolation, cmap = cmap, origin='lower',vmin=-1,vmax=1,zorder=1)
	width=0.0025
	scale=2.0

	Q = ax.quiver(mx.T,my.T,pivot='mid',zorder=2,width=width, scale=scale, angles='xy', scale_units='xy')

	fig.colorbar(im, label=r'$m_z$',orientation='vertical')

	plt.show()	

#@todo: remove - deprecated
def oldSpins2D(spinLattice, spinPositions):
	fig, ax = plt.subplots(figsize=(6,6))
	
	x = np.zeros(params.spinsTotal)
	y = np.zeros(params.spinsTotal)
	sx = np.zeros(params.spinsTotal)
	sy = np.zeros(params.spinsTotal)
	sz = np.zeros(params.spinsTotal)
	
	"""
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
	"""

	#mx=magdata[-1,1:Nx+1,1:Ny+1,0]
	#my=magdata[-1,1:Nx+1,1:Ny+1,1]
	#mz=magdata[-1,1:Nx+1,1:Ny+1,2]
	
	#@todo: remove this
	#print(spinLattice)
	sx = spinLattice[:,:,0]
	sy = spinLattice[:,:,1]
	sz = spinLattice[:,:,2]

	ax.quiver(sx, sy, scale = 2, angles='xy', scale_units='xy')
	im = ax.imshow(sz, cmap='bwr', vmin=-1, vmax=1)
	ax.set_ylim(ax.get_ylim()[1], ax.get_ylim()[0])
	
	fig.colorbar(im, ax=ax)

	plt.show()
	

#@TODO: fix spin positions (must be a square lattice)
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
		z[k] = 0

		sx[k] = mx[k][size-1]
		sy[k] = my[k][size-1]
		sz[k] = mz[k][size-1]

	cx.quiver(x, y, z, sx, sy, sz, length=0.05, normalize=True)
	plt.show()