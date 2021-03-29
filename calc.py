import numpy as np
import params
import sys

def euler(spin, spinLattice, x, y):
	magx = spin[0]
	magy = spin[1]
	magz = spin[2]

	spin[0] = magx / np.sqrt(magx**2 + magy**2 + magz**2)
	spin[1] = magy / np.sqrt(magx**2 + magy**2 + magz**2)
	spin[2] = magz / np.sqrt(magx**2 + magy**2 + magz**2)

	H = Heff(spin, spinLattice, x, y)
	result = np.cross(spin, H)
	
	spin[0] = spin[0] + params.h*result[0]
	spin[1] = spin[1] + params.h*result[1]
	spin[2] = spin[2] + params.h*result[2]
	
	spinLattice[x][y] = spin

	return spin
	
def Heff(spin, spinLattice, x, y):
	_lambda = 1
	A = 1
	B = 1
	C = 1

	#anisotropyInteraction = A*spin[0] + B*spin[1] + C*spin[2]

	term1 = np.add(exchangeInteraction(spinLattice, spin, x, y), params.H) 
	term2 = np.cross(_lambda * term1, spin)

	return np.add(term1, term2)

def exchangeInteraction(spinLattice, spin, X, Y):
	J = 1
	Nx = params.Nx
	Ny = params.Ny
	
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
