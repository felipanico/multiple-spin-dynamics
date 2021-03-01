import numpy as np
import math
import sys
from matplotlib import pyplot as plt

# global variables
n = 100
h = 0.05
Nx = 5
Ny = 5
H = np.array([0,0,1])
position = 1.0 / np.sqrt(3.0)

# begin functions
mx = []
my = []
mz = []
def euler(spin, x, y):
	result = derivate(spin, Heff(spin,H))
	spin[0] = spin[0] + h*result[0]
	spin[1] = spin[1] + h*result[1]
	spin[2] = spin[2] + h*result[2]
	spinLattice[x][y] = spin
	mx.append(spin[0])
	my.append(spin[1])
	mz.append(spin[2])

def giromagneticRatio():
	k = 1 #numeric value is 1.76*10**(11)
	u0 = 1 #numeric value is 1.2566*10**(-6)

	return k*u0*(-1) #check the signal

def derivate(S,H):
	return giromagneticRatio()*(np.cross(S,H))

def Heff(S,H):
	lamb = 0.1 #lambda is reserved world

	return np.add(H, lamb * np.cross(S,H))

def createSpinLattice():
	for x in range(Nx):
		for y in range(Ny):
			spinLattice[x][y] = [x,y,0]
	
	return spinLattice


def plotM(mx, my, mz):
	plt.plot(mx, label = 'mx')
	plt.plot(my, label = 'my')
	plt.plot(mz, label = 'mz')
	plt.title('Magnetization')
	plt.show()

def plotInitialPositions():
	sx = spinLattice[:,:,0]
	sy = spinLattice[:,:,1]
	fig, ax = plt.subplots(figsize=(7,7))
	width=0.003
	scale=1.0
	ax.quiver(sx,sy, pivot='mid',width=width)

	ax.xaxis.set_ticks([])
	ax.yaxis.set_ticks([])
	ax.set_aspect('equal')
	plt.show()

def plotFinalPositions():
	sx = spinLattice[:,:,0]
	sy = spinLattice[:,:,1]
	fig2, bx = plt.subplots(figsize=(7,7))
	width=0.003
	scale=1.0
	bx.quiver(sx,sy, pivot='mid',width=width)
	bx.xaxis.set_ticks([])
	bx.yaxis.set_ticks([])
	bx.set_aspect('equal')
	plt.show()		

#end functions

#main program
spinLattice = np.zeros((Nx+2,Ny+2,3),np.float64)[1:Nx+1,1:Ny+1,:]
createSpinLattice()

plotInitialPositions()

for t in range(n-1):
	for x in range(Nx):
		for y in range(Ny):
			euler(spinLattice[x][y], x, y)

plotFinalPositions()
plotM(mx,my,mz)