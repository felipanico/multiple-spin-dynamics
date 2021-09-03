import numpy as np
import sys
import params

def minimization(initialSpins, finalSpins):
	for i in range(params.Nx):
		for j in range(params.Ny):
			result = hamiltonian(initialSpins, i + 1,j + 1)
			finalSpins[i + 1][j + 1] = np.copy(result)
			
	return finalSpins

def hamiltonian(spinLattice, i, j):
	Hex = np.copy(exchangeInteraction(spinLattice, i, j))
	
	energy = spinLattice[i][j] * Hex
	energy = energy[0] + energy[1] + energy[2]

	return Hex,energy
	
def exchangeInteraction(spinLattice, i, j):
	result = np.array([0,0,0],  np.longdouble)

	result[0] = params.J*(np.copy(spinLattice[i-1][j][0]) + np.copy(spinLattice[i+1][j][0]) + np.copy(spinLattice[i][j-1][0]) + np.copy(spinLattice[i][j+1][0]))
	result[1] = params.J*(np.copy(spinLattice[i-1][j][1]) + np.copy(spinLattice[i+1][j][1]) + np.copy(spinLattice[i][j-1][1]) + np.copy(spinLattice[i][j+1][1]))
	result[2] = params.J*(np.copy(spinLattice[i-1][j][2]) + np.copy(spinLattice[i+1][j][2]) + np.copy(spinLattice[i][j-1][2]) + np.copy(spinLattice[i][j+1][2]))

	return result


def dmInteraction(spinLattice, i, j):
	D = params.D
	result = np.array([0,0,0],  np.longdouble)

	result[0] = D*(np.copy(spinLattice[i][j-1][2]) - np.copy(spinLattice[i][j+1][2]))
	result[1] = D*(np.copy(spinLattice[i+1][j][2]) - np.copy(spinLattice[i-1][j][2]))
	result[2] = D*(np.copy(spinLattice[i][j+1][0]) - np.copy(spinLattice[i+1][j][1]) - np.copy(spinLattice[i][j-1][0]) + np.copy(spinLattice[i-1][j][1]))

	return result
