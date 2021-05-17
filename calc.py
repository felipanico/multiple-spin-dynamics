import numpy as np
import params
import lattice
import sys

def euler(spinLattice, x, y):
	spin = spinLattice[x][y]
	
	magx = spin[0]
	magy = spin[1]
	magz = spin[2]

	#if (magx > 0 and magy > 0 and magz > 0):
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

	Heff = params.H + exchangeInteraction(spinLattice, x, y)

	SxHeff = np.cross(spin, Heff)

	SxSxHeff = np.cross(spin, SxHeff)

	return -SxHeff - alpha*SxSxHeff

def exchangeInteraction(spinLattice, i, j):
	J = params.J

	iMinus, i, iPlus, jMinus, j, jPlus = lattice.createPbc(i,j)

	beff = np.zeros(3, np.float64)
	grid = np.copy(spinLattice)
	contJ = j + 1
	contI = i + 1

	iMinus = contI - 1
	if (contI == 1):
		iMinus = params.Nx+1

	iPlus = contI + 1
	if (contI == params.Nx):
		iPlus = 1

	jMinus = contJ - 1
	if (contJ == 1):
		jMinus = params.Ny+1

	jPlus = contI + 1
	if (contJ == params.Ny):
		jPlus = 1	
	
	beff[0] = grid[iMinus][contJ][0] + grid[iPlus][contJ][0] + grid[contI][jMinus][0] + grid[contI][jPlus][0]
	beff[1] = grid[iMinus][contJ][1] + grid[iPlus][contJ][1] + grid[contI][jMinus][1] + grid[contI][jPlus][1]
	beff[2] = grid[iMinus][contJ][2] + grid[iPlus][contJ][2] + grid[contI][jMinus][2] + grid[contI][jPlus][2]
	
	return J*beff

def dmInteraction(spinLattice, x, y):
	D = -params.D

	spinInteraction = np.zeros(3, np.float64)

	lineDown, line, lineUp, columnLeft, column, columnRight = lattice.createPbc(x,y)
	
	spinInteraction[0] = D*(spinLattice[lineDown][column][2] - spinLattice[lineUp][column][2])
	spinInteraction[1] = D*(spinLattice[line][columnRight][2] - spinLattice[line][columnLeft][2])
	spinInteraction[2] = D*(spinLattice[lineUp][column][0] - spinLattice[line][columnRight][1] - spinLattice[lineDown][column][0] + spinLattice[line][columnLeft][1])

	return spinInteraction
