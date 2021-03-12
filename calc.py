import numpy as np

def euler(H, spinLattice, spin, x, y, h):
	result = derivate(spin, Heff(spin,H))
	spin[0] = spin[0] + h*result[0]
	spin[1] = spin[1] + h*result[1]
	spin[2] = spin[2] + h*result[2]
	spinLattice[x][y] = spin
	
	return spin
	
def giromagneticRatio():
	k = 1 #numeric value is 1.76*10**(11)
	u0 = 1 #numeric value is 1.2566*10**(-6)

	return k*u0*(-1) #check the signal

def derivate(S,H):
	return giromagneticRatio()*(np.cross(S,H))

def Heff(S,H):
	lamb = 0.1 #lambda is reserved world

	return np.add(H, lamb * np.cross(S,H))