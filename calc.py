import numpy as np
import params
import lattice
import sys

def euler(spinLattice, x, y):
	spin = spinLattice[x][y]

	magx = spin[0]
	magy = spin[1]
	magz = spin[2]

	spin[0] = magx / np.sqrt(magx**2 + magy**2 + magz**2)
	spin[1] = magy / np.sqrt(magx**2 + magy**2 + magz**2)
	spin[2] = magz / np.sqrt(magx**2 + magy**2 + magz**2)

	result = LLG(spin, spinLattice, x, y)

		
	spin[0] = spin[0] + params.h*result[0]
	spin[1] = spin[1] + params.h*result[1]
	spin[2] = spin[2] + params.h*result[2]

	return spin
	
def LLG(spin, spinLattice, x, y):
	alpha = params.alpha

	Heff = params.H + exchangeInteraction(spinLattice, x, y)

	SxHeff = np.cross(spin, Heff)

	SxSxHeff = np.cross(spin, SxHeff)

	return -SxHeff - alpha*SxSxHeff

def exchangeInteraction(spinLattice, X, Y):
	J = -params.J

	lineDown, line, lineUp, columnLeft, column, columnRight = lattice.createPbc(X,Y)

	spinInteraction = np.zeros(3, np.float64)

	spinInteraction = spinLattice[lineDown][columnLeft] + spinLattice[lineDown][column] + spinLattice[lineDown][columnRight]
	spinInteraction += spinLattice[line][columnLeft] + spinLattice[line][column] + spinLattice[line][columnRight]
	spinInteraction += spinLattice[lineUp][columnLeft] + spinLattice[lineUp][column] + spinLattice[lineUp][columnRight]

	#spinInteraction[0] = J*(spinLattice[line][columnLeft][0] + spinLattice[line][columnRight][0] + spinLattice[lineDown][column][0] + spinLattice[lineUp][column][0])
	#spinInteraction[1] = J*(spinLattice[line][columnLeft][1] + spinLattice[line][columnRight][1] + spinLattice[lineDown][column][1] + spinLattice[lineUp][column][1])
	#spinInteraction[2] = J*(spinLattice[line][columnLeft][2] + spinLattice[line][columnRight][2] + spinLattice[lineDown][column][2] + spinLattice[lineUp][column][2])

	return J*spinInteraction

def dmInteraction(spinLattice, x, y):
	D = -params.D

	spinInteraction = np.zeros(3, np.float64)

	lineDown, line, lineUp, columnLeft, column, columnRight = lattice.createPbc(x,y)
	
	spinInteraction[0] = D*(spinLattice[lineDown][column][2] - spinLattice[lineUp][column][2])
	spinInteraction[1] = D*(spinLattice[line][columnRight][2] - spinLattice[line][columnLeft][2])
	spinInteraction[2] = D*(spinLattice[lineUp][column][0] - spinLattice[line][columnRight][1] - spinLattice[lineDown][column][0] + spinLattice[line][columnLeft][1])

	return spinInteraction
