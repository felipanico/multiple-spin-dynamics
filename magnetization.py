import numpy as np
import math
import sys
from matplotlib import pyplot as plt

# global variables
n = 100
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
			spinLattice[x][y] = [position,position,position]
	
	return spinLattice


def plot(mx, my, mz):
	plt.plot(mx, label = 'mx')
	plt.plot(my, label = 'my')
	plt.plot(mz, label = 'mz')
	plt.title('Magnetization')
	plt.show()

#end functions

#main program
mx = []
my = []
mz = []

spinLattice = np.zeros((Nx+2,Ny+2,3),np.float64)[1:Nx+1,1:Ny+1,:]
createSpinLattice()

for t in range(n-1):
	for x in range(Nx):
		for y in range(Ny):
			euler(spinLattice[x][y], x, y)


for t in (range(n-1)):
	print(mx)
	sys.exit()

