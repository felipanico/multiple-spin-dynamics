import numpy as np
import sys

def euler(H, spinLattice, spin, x, y, h, spinTotal, index, mx, my, mz):
	result = derivate(spin, Heff(spin, spinLattice , H, spinTotal, index, mx, my, mz))
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
	return np.cross(S,H)

def Heff(S, spinLattice, H, spinTotal, index, mx, my,mz):
	lamb = 0.1 #lambda is reserved world
	J = 1
	A = 1
	B = 1
	C = 1
	
	S[0] = A*S[0]
	S[1] = B*S[1]
	S[2] = C*S[2]
	
	sx = np.zeros((spinTotal))
	sy = np.zeros((spinTotal))
	sz = np.zeros((spinTotal))

	for k in range(spinTotal):
		sx[k] = mx[k][index-1]
		sy[k] = my[k][index-1]
		sz[k] = mz[k][index-1]
	
	term1 = np.add(exchangeInteraction(sx, sy, sz, index, k), S) 
	term1 = np.add(term1, H)
	
	term2 = lamb * np.cross(term1, S)

	Heff = np.add(term1, term2)

	return Heff

def exchangeInteraction(sx, sy, sz, index, spinTotal):
	
	J = 1
	
	for k in range(spinTotal):
		isSpinInEdge = 0		
		
		if (k == 0):
			isSpinInEdge = 1
			previousSpinIndex = spinTotal
			nextSpinIndex = k+1	
		
		if (k == spinTotal):
			isSpinInEdge = 1
			nextSpinIndex = 0
			previousSpinIndex = k-1

		if (isSpinInEdge == 0):
			previousSpinIndex = k-1	
			nextSpinIndex = k+1	

		spinInteractionX = sx[previousSpinIndex] + sx[k] + sx[nextSpinIndex]
		spinInteractionY = sy[previousSpinIndex] + sy[k] + sy[nextSpinIndex]
		spinInteractionZ = sz[previousSpinIndex] + sz[k] + sz[nextSpinIndex]
		
		spinInteraction = [spinInteractionX, spinInteractionY, spinInteractionZ]
		
	return J*spinInteraction
	 