import numpy as np
import sys

def euler(spin, spinLattice, H, spinTotal, index, mx, my, mz, h, x, y):
	magx = spin[0]
	magy = spin[1]
	magz = spin[2]

	spin[0] = (magx / np.sqrt(magx**2 + magy**2 + magz**2))
	spin[1] = (magy / np.sqrt(magx**2 + magy**2 + magz**2))
	spin[2] = (magz / np.sqrt(magx**2 + magy**2 + magz**2))

	H = Heff(spin, spinLattice , H, spinTotal, index, mx, my, mz)
	result = derivate(spin, H)
	
	spin[0] = spin[0] + h*result[0]
	spin[1] = spin[1] + h*result[1]
	spin[2] = spin[2] + h*result[2]
	
	spinLattice[x][y] = spin

	return spin
	
def Heff(S, spinLattice, H, spinTotal, index, mx, my,mz):
	_lambda = 0.1
	J = 1
	A = 1
	B = 1
	C = 1

	S[0] = A*S[0]
	S[1] = B*S[1]
	S[2] = C*S[2]

	term1 = np.add(exchangeInteraction(index, spinTotal, spinLattice, S), S) 
	term1 = np.add(term1, H)

	term2 = _lambda * np.cross(term1, S)

	Heff = np.add(term1, term2)

	return Heff

def exchangeInteraction(index, spinTotal, spinLattice, spin):

	J = 1
	Nx = Ny = 3
	X = Y = 0
	
	for x in range(Nx):	
		for y in range(Ny):
			
			S = spinLattice[x][y]
			
			if (S[0] == spin[0] and S[1] == spin[1]):
				X = x
				Y = y
				break;
		
	
	lineDown = X-1
	line = X
	lineUp = X+1
	
	columnRight = Y-1
	column = Y
	columnLeft = Y+1

	if (lineDown <= 0):
		lineDown = Nx -1

	if (lineDown >= Nx):
		lineDown = 0

	if (lineUp <= 0):
		lineUp = Nx - 1 

	if (lineUp >= Nx):
		lineUp = 0

	if (columnLeft >= Ny ):
		columnLeft = 0

	if (columnLeft <= 0 ):
		columnLeft = Ny - 1				    		

	if (columnRight >= Ny):
		columnRight = 0

	if (columnRight <= 0):
		columnRight = Ny - 1	
	
	spinInteraction = spinLattice[lineDown][columnLeft] + spinLattice[lineDown][column] + spinLattice[lineDown][columnRight]
	spinInteraction += spinLattice[line][columnLeft] + spinLattice[line][column] + spinLattice[line][columnRight]
	spinInteraction += spinLattice[lineUp][columnLeft] + spinLattice[lineUp][column] + spinLattice[lineUp][columnRight]
		
	return J*spinInteraction


def giromagneticRatio():
	k = 1 #numeric value is 1.76*10**(11)
	u0 = 1 #numeric value is 1.2566*10**(-6)

	return k*u0*(-1) #check the signal

def derivate(S,H):
	return np.cross(S,H)
	 
