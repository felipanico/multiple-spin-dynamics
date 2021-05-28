import numpy as np
import params
import lattice
import sys
from bigfloat import *

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
	Heff = params.H + Hdm

	spin = np.copy(spinLattice[i][j])

	print("mag old", spin)
	
	SxHeff = np.cross(spin, Heff)

	SxSxHeff = np.cross(spin, SxHeff)
	
	result[0] =  -SxHeff[0] - alpha*SxSxHeff[0]
	result[1] =  -SxHeff[1] - alpha*SxSxHeff[1]
	result[2] =  -SxHeff[2] - alpha*SxSxHeff[2]

	spin[0] = spin[0] + params.h*result[0]
	spin[1] = spin[1] + params.h*result[1]
	spin[2] = spin[2] + params.h*result[2]

	#spin = np.array([BigFloat(spin[0]), BigFloat(spin[1]), BigFloat(spin[2])])

	#print("Heff", Heff)
	#print("mag new", spin)
	
	return spin

def dmInteraction(spinLattice, i, j):
	D = params.D

	
	"""
	print('spin Lattice')
	print(spinLattice)
	
	print('i value', i)
	print('j value', j)
	print('j-1', spinLattice[i][j-1])
	print('j+1', spinLattice[i][j+1])
	print('i+1', spinLattice[i+1][j])
	print('i-1', spinLattice[i-1][j])

	"""
	
	sx = D*np.copy(spinLattice[i][j-1][2]) - np.copy(spinLattice[i][j+1][2])
	sy = D*np.copy(spinLattice[i+1][j][2]) - np.copy(spinLattice[i-1][j][2])
	sz = D*np.copy(spinLattice[i][j+1][0]) - np.copy(spinLattice[i+1][j][1]) - np.copy(spinLattice[i][j-1][0]) + np.copy(spinLattice[i-1][j][1])

	#print("Beff", np.array([sx,sy,sz]))
	
	return D*np.array([sx,sy,sz])