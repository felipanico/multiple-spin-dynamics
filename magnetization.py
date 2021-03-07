import numpy as np
import math
import sys
from matplotlib import pyplot as plt

# global variables
n = 1000
h = 0.05
Nx = 2
Ny = 2
H = np.array([0,0,1])
position = 1.0 / np.sqrt(3.0)

# begin functions
def euler(spin, x, y):
	result = derivate(spin, Heff(spin,H))
	spin[0] = spin[0] + h*result[0]
	spin[1] = spin[1] + h*result[1]
	spin[2] = spin[2] + h*result[2]
	spinLattice[x][y] = spin
	return spin
	
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
	for i in range(Nx):
		for j in range(Ny):
			k = i + j
			spinLattice[i][j] = [i+1, j+1, k+1]

def createSpinPosition():
	for i in range(Nx):
		for j in range(Ny):
			spinPosition[i][j] = [i, j, 0]

def plotMagnetization(mx, my, mz):
	plt.plot(mx, label = 'mx')
	plt.plot(my, label = 'my')
	plt.plot(mz, label = 'mz')
	plt.title('Magnetization')
	plt.show()


sx = []
sy = []
sz = []
def plotInitialPositions():
	sx = spinLattice[:,:,0]
	sy = spinLattice[:,:,1]
	sz = spinLattice[:,:,2]
	fig, ax = plt.subplots(figsize=(7,7))
	width=0.003
	ax.quiver(sx,sy,sz, pivot='mid',width=width)
	ax.xaxis.set_ticks([])
	ax.yaxis.set_ticks([])
	ax.set_aspect('equal')
	plt.show()

def plotFinalPositions():
	sx = spinLattice[:,:,0]
	sy = spinLattice[:,:,1]
	sz = spinLattice[:,:,2]
	fig2, bx = plt.subplots(figsize=(7,7))
	width=0.003
	bx.quiver(sx,sy,sz, pivot='mid', width=width)
	bx.xaxis.set_ticks([])
	bx.yaxis.set_ticks([])
	bx.set_aspect('equal')
	plt.show()

def createFinalSpinLattice(size):
	finalSpinLattice = np.zeros((size,2,3),np.float64)
	
	for k in range(size):
		finalSpinLattice[k][0] = mx[k], my[k], mz[k]
		finalSpinLattice[k][1] = mx[k+1], my[k+1], mz[k+1]
	
	return finalSpinLattice
#end functions

#main program
mx = np.zeros((Nx*Ny,n-1))
my = np.zeros((Nx*Ny,n-1))
mz = np.zeros((Nx*Ny,n-1))

spinLattice = np.zeros((Nx+2,Ny+2,3),np.float64)[1:Nx+1,1:Ny+1,:]
spinPosition = np.zeros((Nx+2,Ny+2,3),np.float64)[1:Nx+1,1:Ny+1,:]
createSpinLattice()

for t in range(n-1):
	i = 0
	for x in range(Nx):
		for y in range(Ny):
			spin = euler(spinLattice[x][y], x, y)
			mx[i][t] = spin[0]
			my[i][t] = spin[1]
			mz[i][t] = spin[2]
			i = i+1
			
spinIndex = 0 #index of spin for magnetization plot
plotMagnetization(mx[spinIndex],my[spinIndex],mz[spinIndex])
