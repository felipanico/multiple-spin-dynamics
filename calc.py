import numpy as np
import sys
import params

def llgEvolve(initialSpins, finalSpins):
	for i in range(params.Nx):
		for j in range(params.Ny):
			result = llgSolve(initialSpins, i + 1,j + 1)
			finalSpins[i + 1][j + 1] = np.copy(result)
			
	return finalSpins
	
def llgSolve(spinLattice, i, j):
	alpha = params.alpha
	result = np.array([0,0,0],  np.longdouble)

	Hdm = np.copy(dmInteraction(spinLattice, i, j))
	Hex = np.copy(exchangeInteraction(spinLattice, i, j))
	Heff = params.H + Hdm + Hex

	spin = np.copy(spinLattice[i][j])

	SxHeff = np.cross(spin, Heff)

	SxSxHeff = np.cross(spin, SxHeff)
	
	result[0] =  -SxHeff[0] - alpha*SxSxHeff[0]
	result[1] =  -SxHeff[1] - alpha*SxSxHeff[1]
	result[2] =  -SxHeff[2] - alpha*SxSxHeff[2]

	spin[0] = spin[0] + params.h*result[0]
	spin[1] = spin[1] + params.h*result[1]
	spin[2] = spin[2] + params.h*result[2]

	return spin

def exchangeInteraction(spinLattice, i, j):
	J = params.J
	result = np.array([0,0,0],  np.longdouble)

	result[0] = J*(np.copy(spinLattice[i-1][j][0]) + np.copy(spinLattice[i+1][j][0]) + np.copy(spinLattice[i][j-1][0]) + np.copy(spinLattice[i][j+1][0]))
	result[1] = J*(np.copy(spinLattice[i-1][j][1]) + np.copy(spinLattice[i+1][j][1]) + np.copy(spinLattice[i][j-1][1]) + np.copy(spinLattice[i][j+1][1]))
	result[2] = J*(np.copy(spinLattice[i-1][j][2]) + np.copy(spinLattice[i+1][j][2]) + np.copy(spinLattice[i][j-1][2]) + np.copy(spinLattice[i][j+1][2]))

	#print("Heff", )
	
	return result


def dmInteraction(spinLattice, i, j):
	D = params.D
	result = np.array([0,0,0],  np.longdouble)

	result[0] = D*(np.copy(spinLattice[i][j-1][2]) - np.copy(spinLattice[i][j+1][2]))
	result[1] = D*(np.copy(spinLattice[i+1][j][2]) - np.copy(spinLattice[i-1][j][2]))
	result[2] = D*(np.copy(spinLattice[i][j+1][0]) - np.copy(spinLattice[i+1][j][1]) - np.copy(spinLattice[i][j-1][0]) + np.copy(spinLattice[i-1][j][1]))

	return result