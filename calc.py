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

	print(result)
	sys.exit()

	spin[0] = spin[0] + params.h*result[0]
	spin[1] = spin[1] + params.h*result[1]
	spin[2] = spin[2] + params.h*result[2]

	print(spin)
	#sys.exit()
	
	return spin
	
def LLG(S, spinLattice, x, y):
	alpha = params.alpha

	Heff = np.copy(params.H)

	spin = np.copy(S)
	
	SxHeff = np.cross(spin, Heff)

	SxSxHeff = np.cross(spin, SxHeff)

	return -SxHeff - alpha*SxSxHeff

def exchangeInteractionTest(spinLattice, i, j):
	J = params.J

	beff = np.zeros(3, np.float64)
	grid = np.copy(spinLattice)

	iMinus = i - 1
	if (iMinus <= 0):
		iMinus = params.Nx-1

	iPlus = i + 1
	if (iPlus >= params.Nx):
		iPlus = 0

	jMinus = j - 1
	if (jMinus <= 0):
		jMinus = params.Ny-1

	jPlus = j + 1
	if (jPlus >= params.Ny):
		jPlus = 0

	auxIminus = np.zeros(3, np.float64)
	if (i-1 > 0):
		auxIminus = grid[iMinus]

	auxIplus = np.zeros(3, np.float64)
	if (i+1 < params.Nx):
		auxIplus = grid[iPlus]	

	beff[0] = auxIminus[0] + auxIplus[0] + grid[i][jMinus][0] + grid[i][jPlus][0]
	beff[1] = auxIminus[1] + auxIplus[1] + grid[i][jMinus][1] + grid[i][jPlus][1]
	beff[2] = auxIminus[2] + auxIplus[2] + grid[i][jMinus][2] + grid[i][jPlus][2]

	return J*beff

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
