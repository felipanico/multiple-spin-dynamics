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
	gamma = params.gamma

	#Heff = np.copy(params.H) + exchangeInteraction(spinLattice, x, y)

	#Heff = np.copy(params.H + dmInteraction(spinLattice, x, y) + exchangeInteraction(spinLattice, x, y))
	
	Heff = np.copy(dmInteraction(spinLattice, x, y))
	
	S = np.copy(spin)
	
	SxHeff = np.cross(S, Heff)

	SxSxHeff = np.cross(S, SxHeff)

	return -SxHeff - alpha*SxSxHeff

def exchangeInteraction(spinLattice, x, y):
	J = -params.J
	
	lineDown, line, lineUp, columnLeft, column, columnRight = lattice.createPbc(x,y)
	
	sx = np.copy(spinLattice[lineUp][column][0]) + np.copy(spinLattice[lineDown][column][0]) + np.copy(spinLattice[line][columnRight][0]) + np.copy(spinLattice[line][columnLeft][0])
	sy = np.copy(spinLattice[lineUp][column][1]) + np.copy(spinLattice[lineDown][column][1]) + np.copy(spinLattice[line][columnRight][1]) + np.copy(spinLattice[line][columnLeft][1])
	sz = np.copy(spinLattice[lineUp][column][2]) + np.copy(spinLattice[lineDown][column][2]) + np.copy(spinLattice[line][columnRight][2]) + np.copy(spinLattice[line][columnLeft][2])
	
	return J*np.array([sx,sy,sz])

def dmInteraction(spinLattice, x, y):
	D = -params.D

	lineDown, line, lineUp, columnLeft, column, columnRight = lattice.createPbc(x,y)
	
	#second version
	sx = np.copy(spinLattice[lineDown][column][2]) - np.copy(spinLattice[lineUp][column][2])
	sy = np.copy(spinLattice[line][columnRight][2]) - np.copy(spinLattice[line][columnLeft][2])
	sz = np.copy(spinLattice[lineUp][column][0]) - np.copy(spinLattice[line][columnRight][1]) - np.copy(spinLattice[lineDown][column][0]) + np.copy(spinLattice[line][columnLeft][1])
	
	# first version
	#sx = np.copy(spinLattice[line][columnLeft][2]) - np.copy(spinLattice[line][columnRight][2])
	#sy = np.copy(spinLattice[lineUp][column][2]) - np.copy(spinLattice[lineDown][column][2])
	#sz = np.copy(spinLattice[line][columnRight][0]) - np.copy(spinLattice[lineUp][column][1]) - np.copy(spinLattice[line][columnLeft][0]) + np.copy(spinLattice[lineDown][column][1])

	return D*np.array([sx,sy,sz])
