import numpy as np
import sys
import params

def llgEvolve(initialSpins, finalSpins):
	for i in range(params.Nx):
		for j in range(params.Ny):
			result = llgSolve(initialSpins, i + 1,j + 1)
			finalSpins[i + 1][j + 1] = np.copy(result)
			
	return finalSpins

def LLG(spin, spinLattice, i, j):
	result = np.array([0,0,0],  np.longdouble)
	Hdm = np.copy(dmInteraction(spinLattice, i, j))
	Hex = np.copy(exchangeInteraction(spinLattice, i, j))
	
	Heff = params.H + Hex + Hdm

	SxHeff = np.cross(spin, Heff)

	SxSxHeff = np.cross(spin, SxHeff)

	result[0] = SxHeff[0] - params.alpha*SxSxHeff[0]
	result[1] = SxHeff[1] - params.alpha*SxSxHeff[1]
	result[2] = SxHeff[2] - params.alpha*SxSxHeff[2]

	return result
	
def llgSolve(spinLattice, i, j):
	spin = np.copy(spinLattice[i][j])

	result = LLG(spin, spinLattice, i, j)
	
	k1 = np.copy(result)
    
	k1x = k1[0]
	k1y = k1[1]
	k1z = k1[2]

	result[0] = result[0] + params.h
	result[1] = result[1] + params.h * k1y
	result[2] = result[0] + params.h * k1z

	k2 = params.h * LLG(result, spinLattice, i, j)
	
	k2x = k2[0]
	k2y = k2[1]
	k2z = k2[2]

	spin[0] = spin[0] + (params.h/2) * (k1x + k2x) 
	spin[1] = spin[1] + (params.h/2) * (k1y + k2y) 
	spin[2] = spin[2] + (params.h/2) * (k1z + k2z) 

	return spin

def exchangeInteraction(spinLattice, i, j):
	J = params.J
	result = np.array([0,0,0],  np.longdouble)

	result[0] = J*(np.copy(spinLattice[i-1][j][0]) + np.copy(spinLattice[i+1][j][0]) + np.copy(spinLattice[i][j-1][0]) + np.copy(spinLattice[i][j+1][0]))
	result[1] = J*(np.copy(spinLattice[i-1][j][1]) + np.copy(spinLattice[i+1][j][1]) + np.copy(spinLattice[i][j-1][1]) + np.copy(spinLattice[i][j+1][1]))
	result[2] = J*(np.copy(spinLattice[i-1][j][2]) + np.copy(spinLattice[i+1][j][2]) + np.copy(spinLattice[i][j-1][2]) + np.copy(spinLattice[i][j+1][2]))

	return result


def dmInteraction(spinLattice, i, j):
	D = params.D
	result = np.array([0,0,0],  np.longdouble)

	result[0] = D*(np.copy(spinLattice[i][j-1][2]) - np.copy(spinLattice[i][j+1][2]))
	result[1] = D*(np.copy(spinLattice[i+1][j][2]) - np.copy(spinLattice[i-1][j][2]))
	result[2] = D*(np.copy(spinLattice[i][j+1][0]) - np.copy(spinLattice[i+1][j][1]) - np.copy(spinLattice[i][j-1][0]) + np.copy(spinLattice[i-1][j][1]))

	return result
