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

def spins2DT(magdata):
	fig, ax = plt.subplots(figsize=(6,6))
	interpolation='nearest'
	cmap=plt.get_cmap('coolwarm_r')
	Nx = params.Nx
	Ny = params.Ny

	mx=magdata[0:Nx,0:Ny,0]
	my=magdata[0:Nx,0:Ny,1]
	mz=magdata[0:Nx,0:Ny,2]
	
	im=ax.imshow(my.T,interpolation=interpolation, cmap = cmap, origin='lower',vmin=-1,vmax=1,zorder=1)
	width=0.0025
	scale=2.0

	Q = ax.quiver(mx.T,mz.T,pivot='mid',zorder=2,width=width, scale=scale, angles='xy', scale_units='xy')

	fig.colorbar(im, label=r'$m_z$',orientation='vertical')

	plt.show()