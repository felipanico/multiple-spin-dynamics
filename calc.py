import numpy as np
import params
import lattice
import sys

def euler(spinLattice, x, y):
	spin = spinLattice[x][y]

	magx = spin[0]
	magy = spin[1]
	magz = spin[2]

	#spin[0] = magx / np.sqrt(magx**2 + magy**2 + magz**2)
	#spin[1] = magy / np.sqrt(magx**2 + magy**2 + magz**2)
	#spin[2] = magz / np.sqrt(magx**2 + magy**2 + magz**2)

	result = LLG(spin, spinLattice, x, y)
	
	spin[0] = spin[0] + params.h*result[0]
	spin[1] = spin[1] + params.h*result[1]
	spin[2] = spin[2] + params.h*result[2]

	return spin
	
def LLG(spin, spinLattice, x, y):
	alpha = params.alpha

	Heff = dmInteraction(spinLattice, x, y)
	
	SxHeff = np.cross(spin, Heff)

	SxSxHeff = np.cross(spin, SxHeff)

	return -SxHeff - alpha*SxSxHeff

def exchangeInteraction(spinLattice, X, Y):
	J = params.J

	lineDown, line, lineUp, columnLeft, column, columnRight = lattice.createPbc(X,Y)

	spinInteraction = np.zeros(3, np.float64)
	
	spinInteraction[0] = J*(spinLattice[line][columnLeft][0] + spinLattice[line][columnRight][0] + spinLattice[lineDown][column][0] + spinLattice[lineUp][column][0])
	spinInteraction[1] = J*(spinLattice[line][columnLeft][1] + spinLattice[line][columnRight][1] + spinLattice[lineDown][column][1] + spinLattice[lineUp][column][1])
	spinInteraction[2] = J*(spinLattice[line][columnLeft][2] + spinLattice[line][columnRight][2] + spinLattice[lineDown][column][2] + spinLattice[lineUp][column][2])

	return spinInteraction

def dmInteraction(spinLattice, X, Y):
	D = params.D

	#beff[0] += dmi*(mag[indz(i,j-1)]-mag[indz(i,j+1)]);
	#beff[1] += dmi*(mag[indz(i+1,j)]-mag[indz(i-1,j)]);
	#beff[2] += dmi*(mag[indx(i,j+1)]-mag[indy(i+1,j)]-mag[indx(i,j-1)]+mag[indy(i-1,j)]);
	
	lineDown, line, lineUp, columnLeft, column, columnRight = lattice.createPbc(X,Y)

	#spinInteraction = np.zeros(3, np.float64)
	
	#spinInteraction = D*(spinLattice[lineUp][column][2] - spinLattice[lineDown][column][2])
	#spinInteraction = D*(spinLattice[line][columnRight][2] + spinLattice[line][columnLeft][2])
	#spinInteraction = D*(spinLattice[lineUp][column][0] - spinLattice[line][columnRight][1] - spinLattice[lineDown][column][0] + spinLattice[line][columnLeft][1])

	spinInteraction = spinLattice[lineUp][column] - spinLattice[lineDown][column]
	spinInteraction += spinLattice[line][columnLeft] 
	spinInteraction += spinLattice[line][columnRight]
	
	return spinInteraction
