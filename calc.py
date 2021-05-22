import numpy as np
import params
import lattice
import sys

def euler(spinLattice, x, y):
	spin = spinLattice[x + 1][y + 1]
	
	magx = spin[0]
	magy = spin[1]
	magz = spin[2]

	#if (magx > 0 and magy > 0 and magz > 0):
	#	spin[0] = magx / np.sqrt(magx**2 + magy**2 + magz**2)
	#	spin[1] = magy / np.sqrt(magx**2 + magy**2 + magz**2)
	#	spin[2] = magz / np.sqrt(magx**2 + magy**2 + magz**2)

	result = LLG(spin, spinLattice, x, y)

	spin[0] = spin[0] + params.h*result[0]
	spin[1] = spin[1] + params.h*result[1]
	spin[2] = spin[2] + params.h*result[2]

	return spin
	
def LLG(spin, spinLattice, x, y):
	alpha = params.alpha

	Heff = params.H

	SxHeff = np.cross(spin, Heff)

	SxSxHeff = np.cross(spin, SxHeff)

	
	return -SxHeff - alpha*SxSxHeff

def dmInteraction(spinLattice, x, y):
	D = params.D

	lineDown, line, lineUp, columnLeft, column, columnRight = lattice.createPbc(x,y)

	if (line - 1 < 0):
		lineDown = params.Nx

	if (line + 1 >= params.Nx):
		lineUp = 0

	lineUp = lineUp + 1
	lineDown = lineDown + 1
	line = line + 1
		
	column = column + 1
	if (column - 1 < params.Ny):
		columnLeft = params.Nx -1

	if (column + 1 > params.Nx):
		columnRight = 1
	
	
	#print('i,j', spinLattice[line][column])
	#print('i,j-1', spinLattice[line][columnLeft])
	#print('i,j+1', spinLattice[line][columnRight])
	#print(lineUp)
	#print('i+1,j', spinLattice[lineUp][column])
	#print('i-1,j', spinLattice[lineDown][column])
	
	#test
	#sx = np.copy(spinLattice[line][columnLeft][2]) - np.copy(spinLattice[line][columnRight][2])
	#sy = np.copy(spinLattice[lineUp][column][2]) - np.copy(spinLattice[lineDown][column][2])
	#sz = np.copy(spinLattice[line][columnRight][0]) - np.copy(spinLattice[lineUp][column][1]) - np.copy(spinLattice[line][columnLeft][0]) + np.copy(spinLattice[lineDown][column][1])

	#second version
	#sx = np.copy(spinLattice[lineDown][column][2]) - np.copy(spinLattice[lineUp][column][2])
	#sy = np.copy(spinLattice[line][columnRight][2]) - np.copy(spinLattice[line][columnLeft][2])
	#sz = np.copy(spinLattice[lineUp][column][0]) - np.copy(spinLattice[line][columnRight][1]) - np.copy(spinLattice[lineDown][column][0]) + np.copy(spinLattice[line][columnLeft][1])
	
	# first version
	sx = np.copy(spinLattice[line][columnLeft][2]) - np.copy(spinLattice[line][columnRight][2])
	sy = np.copy(spinLattice[lineUp][column][2]) - np.copy(spinLattice[lineDown][column][2])
	sz = np.copy(spinLattice[line][columnRight][0]) - np.copy(spinLattice[lineUp][column][1]) - np.copy(spinLattice[line][columnLeft][0]) + np.copy(spinLattice[lineDown][column][1])

	return D*np.array([sx,sy,sz])