import numpy as np
import math
import sys

def euler(H, spinLattice, spin, x, y, h):
	H = Heff(spin, H)
	result = derivate(spin, H)
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
	_lambda = 0.1
	return np.add(H, _lambda * np.cross(S,H))