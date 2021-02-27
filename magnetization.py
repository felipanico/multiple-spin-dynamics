import numpy as np
import math
import sys
from matplotlib import pyplot as plt

# global variables
n = 1000
h = 0.05
H = np.array([0,0,1])

# begin functions
def euler(spin, x, y):
	result = derivate(spin, Heff(spin,H))
	spin[0] = spin[0] + h*result[0]
	spin[1] = spin[1] + h*result[1]
	spin[2] = spin[2] + h*result[2]
	
#	print(spin)
#	sys.exit()
	
	spinLattice[x][y] = spin

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
	for t in range(n-1):
		for x in range(Nx):
			for y in range(Ny):
				spinLattice[x][y] = [x,y,0]
	return spinLattice


def plot():
	plt.plot(sx, label = 'sx')
	plt.plot(sy, label = 'sy')
	plt.plot(sz, label = 'sz')
	plt.title('Multiple Spin')
	plt.show()

#end functions

#main program
position = 1.0 / np.sqrt(3.0)
sx = np.zeros([n])
sy = np.zeros([n])
sz = np.zeros([n])
sx[0] = position
sy[0] = position 
sz[0] = position

Nx = 5
Ny = 5
spinCoordinates = np.zeros((Nx+2,Ny+2,3),np.float64)
spinLattice = spinCoordinates[1:Nx+1,1:Ny+1,:]
createSpinLattice()

for t in range(n-1):
	for x in range(Nx):
		for y in range(Ny):
			spinLattice[x][y] = [x,y,0]
			euler(spinLattice[x][y], x, y)


print(spinLattice)
sys.exit()
			

