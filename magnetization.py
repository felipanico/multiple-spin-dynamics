import numpy as np
import math
import sys
from matplotlib import pyplot as plt

# global variables
n = 300
h = 0.05
Nx = 2
Ny = 2
H = np.array([0,0,10])
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
			spinLattice[i][j] = [i + 1, j + 1, k + 1]

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

	print(spinLattice)
	
	fig, ax = plt.subplots(figsize=(7,7))
	width=0.003
	ax.quiver(sx,sy,sz, pivot='mid',width=width)
	#plt.show()

def plotFinalPositions():
	sx = spinLattice[:,:,0]
	sy = spinLattice[:,:,1]
	sz = spinLattice[:,:,2]
	fig2, bx = plt.subplots(figsize=(7,7))
	width=0.003
	bx.quiver(sx,sy,sz, pivot='mid',width=width)
	plt.show()

def plot3dPositions(sx,sy,sz):
	fig3 = plt.figure()
	cx = fig3.gca(projection='3d')
	
	x = 0
	y = 0
	z = 0

	cx.quiver(x,y,z, sx,sy,sz, length=0.03, normalize=True)
	plt.show()

#end functions

#main program
mx = np.zeros((Nx*Ny,n-1))
my = np.zeros((Nx*Ny,n-1))
mz = np.zeros((Nx*Ny,n-1))

spinLattice = np.zeros((Nx+2,Ny+2,3),np.float64)[1:Nx+1,1:Ny+1,:]
spinLatticeFinal = np.zeros((Nx+2,Ny+2,3),np.float64)[1:Nx+1,1:Ny+1,:]
createSpinLattice()
#plotInitialPositions()

for t in range(n-1):
	i = 0
	for x in range(Nx):
		for y in range(Ny):
			spin = euler(spinLattice[x][y], x, y)
			spinLatticeFinal[x][y] = spin
			mx[i][t] = spin[0]
			my[i][t] = spin[1]
			mz[i][t] = spin[2]
			i = i+1
			
#print(spinLatticeFinal)

plotFinalPositions()

#spinNumber = 0
#sx = mx[spinNumber][t-1]
#sy = my[spinNumber][t-1]
#sz = mz[spinNumber][t-1]
#plot3dPositions(sx, sy, sz)
#plotMagnetization(mx[spinNumber],my[spinNumber],mz[spinNumber])
