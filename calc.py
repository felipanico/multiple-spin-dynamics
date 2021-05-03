import numpy as np
import params
import lattice
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
	LAMBDA = params._lambda

	#term1 = exchangeInteraction(spinLattice, x, y)
	term1 = dmInteraction(spinLattice, x, y) + params.H
	term2 = np.cross(LAMBDA * term1, spin)

	return term1 + term2


def exchangeInteraction(spinLattice, X, Y):
	J = -params.J

	lineDown, line, lineUp, columnLeft, column, columnRight = lattice.createPbc(X,Y)

	spinInteraction = spinLattice[lineUp][column]
	spinInteraction += spinLattice[line][columnLeft]
	spinInteraction += spinLattice[line][columnRight]
	spinInteraction += spinLattice[lineDown][column]
	
	return J*spinInteraction

def dmInteraction(spinLattice, X, Y):
	D = -params.D

	lineDown, line, lineUp, columnLeft, column, columnRight = lattice.createPbc(X,Y)
	
	spinInteraction = spinLattice[lineUp][column]
	spinInteraction -= spinLattice[lineDown][column]
	spinInteraction += spinLattice[line][columnLeft] 
	spinInteraction += spinLattice[line][columnRight]
	
	return D*spinInteraction
