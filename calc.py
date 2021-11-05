import numpy as np
import sys
import params
import lattice

def llgEvolve(initialSpins, finalSpins):
	
	for i in range(params.Nx):
		for j in range(params.Ny):
			finalSpins[i][j] = np.copy(euler(initialSpins, i, j))
			
	return finalSpins

def LLG(spin, spinLattice, i, j):
	result = np.array([0,0,0],  np.longdouble)
	aux = np.array([0,0,0],  np.longdouble)

	Hex = np.copy(vetorialExchange(spinLattice, i, j))
	Hdm = np.copy(vetorialDm(spinLattice, i, j))
	Hz = np.copy(vetorialZeeman())

	K1 = 1
	K2 = 1
	
	Heff =  np.copy(Hex) + np.copy(Hdm) + np.copy(Hz)

	SxHeff = np.cross(spin, Heff)

	djS = np.copy(stt(spinLattice, i, j))

	SxdjS = np.cross(spin, djS)
	
	aux[0] = np.copy(SxHeff[0]) + K1*np.copy(djS[0]) - K2*params.beta * np.copy(SxdjS[0])
	aux[1] = np.copy(SxHeff[1]) + K1*np.copy(djS[1]) - K2*params.beta * np.copy(SxdjS[1])
	aux[2] = np.copy(SxHeff[2]) + K1*np.copy(djS[2]) - K2*params.beta * np.copy(SxdjS[2])

	alphaSxdS = np.copy(diffS(spinLattice, i, j, aux))
	
	result[0] = aux[0] + alphaSxdS[0]
	result[1] = aux[1] + alphaSxdS[1]
	result[2] = aux[2] + alphaSxdS[2]

	return np.array(result, np.longdouble)

def diffS(spinLattice, i, j, v1):
	a = params.alpha
	a2 = a*a
	M = 1
	sx = spinLattice[i][j][0]
	sy = spinLattice[i][j][1] 
	sz = spinLattice[i][j][2]

	sx2 = sx*sx
	sy2 = sy*sy
	sz2 = sz*sz
	M2 = M*M

	denominator = a2*sz2 + a2*sy2 + a2*sx2 + M2

	dsx = ((a2*sx*sz + M*a*sy)*v1[2] +(a2*sx*sy - M*a*sz)*v1[1] + (a2*sx2 + M2)*v1[0]) / denominator
	
	dsy = ((a2*sy*sz - M*a*sx)*v1[2] + (a2*sy2 + M2)*v1[1] + (M*a*sz + a2*sx*sy)*v1[0]) / denominator
	
	dsz = ((a2*sz2 + M2)*v1[2] +(a2*sy*sz + M*a*sx)*v1[1] + (a2*sx*sz - M*a*sy)*v1[0]) / denominator

	return np.array([dsx,dsy,dsz], np.longdouble)
	
def euler(spinLattice, i, j):
	spin = np.copy(spinLattice[i][j])
	result = np.copy(LLG(spin, spinLattice, i, j))

	aux = np.array([0,0,0], np.longdouble)

	aux[0] = np.copy(spin[0]) + params.h*np.copy(result[0])
	aux[1] = np.copy(spin[1]) + params.h*np.copy(result[1]) 
	aux[2] = np.copy(spin[2]) + params.h*np.copy(result[2])

	return np.array(aux, np.longdouble)

def Rk2(spinLattice, i, j):
	spin = np.copy(spinLattice[i][j])
	result = np.copy(LLG(spin, spinLattice, i, j))

	k1 = np.copy(result)

	k1x = k1[0]
	k1y = k1[1]
	k1z = k1[2]

	result[0] = result[0] + params.h * k1x
	result[1] = result[1] + params.h * k1y
	result[2] = result[2] + params.h * k1z

	k2 = np.copy(LLG(result, spinLattice, i, j))

	k2x = k2[0]
	k2y = k2[1]
	k2z = k2[2]

	aux = np.array([0,0,0], np.longdouble)
	
	aux[0] = spin[0] + (params.h/2) * (k1x + k2x) 
	aux[1] = spin[1] + (params.h/2) * (k1y + k2y) 
	aux[2] = spin[2] + (params.h/2) * (k1z + k2z)

	return np.array(aux, np.longdouble)

def Rk4(spinLattice, i, j):
	spin = np.copy(spinLattice[i][j])

	result = LLG(spin, spinLattice, i, j)

	k1 = np.copy(result)
	
	k1x = k1[0]
	k1y = k1[1]
	k1z = k1[2]

	result[0] = np.copy(result[0]) + (k1x*params.h/2)
	result[1] = np.copy(result[1]) + (k1y*params.h/2)
	result[2] = np.copy(result[2]) + (k1z*params.h/2)
	
	k2 = LLG(result, spinLattice, i, j)

	k2x = k2[0]
	k2y = k2[1]
	k2z = k2[2]

	result[0] = np.copy(result[0]) + (k2x*params.h/2)
	result[1] = np.copy(result[1]) + (k2y*params.h/2)
	result[2] = np.copy(result[2]) + (k2z*params.h/2)
	
	k3 = LLG(result, spinLattice, i, j)

	k3x = k3[0]
	k3y = k3[1]
	k3z = k3[2]

	result[0] = np.copy(result[0]) + (k3x*params.h)
	result[1] = np.copy(result[1]) + (k3y*params.h)
	result[2] = np.copy(result[2]) + (k3z*params.h)

	k4 = LLG(result, spinLattice, i, j)

	k4x = k4[0]
	k4y = k4[1]
	k4z = k4[2]

	spin[0] = spin[0] + params.h*(k1x + 2*k2x + 2*k3x + k4x)/6 
	spin[1] = spin[1] + params.h*(k1y + 2*k2y + 2*k3y + k4y)/6 
	spin[2] = spin[2] + params.h*(k1z + 2*k2z + 2*k3z + k4z)/6
	
	return spin


def vetorialExchange(spinLattice, i, j):
	result = np.array([0,0,0],  np.longdouble)

	x1,x2,y1,y2 = lattice.createPBC(i,j)

	result[0] = np.copy(spinLattice[x1][j][0]) + np.copy(spinLattice[x2][j][0]) + np.copy(spinLattice[i][y1][0]) + np.copy(spinLattice[i][y2][0])
	result[1] = np.copy(spinLattice[x1][j][1]) + np.copy(spinLattice[x2][j][1]) + np.copy(spinLattice[i][y1][1]) + np.copy(spinLattice[i][y2][1])
	result[2] = np.copy(spinLattice[x1][j][2]) + np.copy(spinLattice[x2][j][2]) + np.copy(spinLattice[i][y1][2]) + np.copy(spinLattice[i][y2][2])

	return np.array(-params.J*result, np.longdouble) 


def vetorialDm(spinLattice, i, j):
	result = np.array([0,0,0],  np.longdouble)

	x1,x2,y1,y2 = lattice.createPBC(i,j)

	index = [x1,x2,y1,y2]

	xAux = yAux = zAux = 0

	D = params.D

	Dz = 0

	for i_ in range(-1, 2):
		iint = i + i_
		Dy = i_
		
		if iint >= params.Nx: iint = 0
		elif iint < 0: iint = params.Nx - 1
		
		for j_ in range(-1, 2):
			Dx = j_
			jint = j + j_
			
			if jint >= params.Ny: jint = 0
			elif jint < 0: jint = params.Ny - 1

			if (i_ != 0 and j_ != 0): continue

			spin = np.copy(spinLattice[iint][jint])

			xAux = xAux + D*(Dy*spin[2] - Dz*spin[1])
			yAux = yAux + D*(Dz*spin[0] - Dx*spin[2])
			zAux = zAux + D*(Dx*spin[1] - Dy*spin[0])

	return np.array([xAux,yAux, zAux], np.longdouble)

def vetorialZeeman():
    return np.array(-params.H, np.longdouble)

def stt(spinLattice, i, j):
	jx = params.j[0]
	jy = params.j[1]

	x1,x2,y1,y2 = lattice.createPBC(i,j)

	#@todo: inverse x and y

	result = (jy/2)*(np.copy(spinLattice[x2][j]) - np.copy(spinLattice[x1][j])) + (jx/2)*(np.copy(spinLattice[i][y2]) - np.copy(spinLattice[i][y1]))

	return np.array(result, np.longdouble)
	
	


