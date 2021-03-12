import numpy as np
from matplotlib import pyplot as plt

def individualMagnetization(mx, my, mz):
	plt.plot(mx, label = 'mx')
	plt.plot(my, label = 'my')
	plt.plot(mz, label = 'mz')
	plt.title('Magnetization')
	plt.show()

def positions2D(sx, sy, sz):
	fig, ax = plt.subplots(figsize=(7,7))
	width=0.003
	ax.quiver(sx,sy,sz, pivot='mid',width=width)
	plt.show()

def positions3D(size, spinTotal, xAxis, yAxis, zAxis, mx, my, mz):
	fig3 = plt.figure()
	cx = fig3.gca(projection='3d')
	
	sx = np.zeros((spinTotal))
	sy = np.zeros((spinTotal))
	sz = np.zeros((spinTotal))

	for k in range(spinTotal):
		sx[k] = mx[k][size-1]
		sy[k] = my[k][size-1]
		sz[k] = mz[k][size-1]
	
	cx.quiver(xAxis, yAxis, zAxis, sx, sy, sz, length=0.05, normalize=True)
	plt.show()