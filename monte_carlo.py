from hashlib import new
from typing import final
import random
import math
import params
from math import exp
import numpy as np
import lattice
import plot

def calcHam(spins):
    H = 0.0
    for i in range(params.Nx):
        for j in range(params.Ny):
            H += hamiltonian(spins, i, j)
    return H


def metropolis(spins, deffects):
    energy = 0
    energies = []
    T = 20.0
    T2 = 0.02
    dec = 0.9
    Emin = calcHam(spins)
    spinsmin = np.copy(spins)
    spinsnew = np.copy(spins)
    energy0 = calcHam(spins)
    print(f"Starting Energy MT: {Emin:5f}")

    while (T > T2):
        for step in range(params.n):
            x = np.random.randint(0, params.Nx)
            y = np.random.randint(0, params.Ny)
                
            spinsnew[x,y][0] = np.copy(spins[x,y][0]) + math.sqrt(T)*(2.0 * random.random() - 1.0)
            spinsnew[x,y][1] = np.copy(spins[x,y][1]) + math.sqrt(T)*(2.0 * random.random() - 1.0) 
            spinsnew[x,y][2] = np.copy(spins[x,y][2]) + math.sqrt(T)*(2.0 * random.random() - 1.0)

            magx = spinsnew[x,y][0]
            magy = spinsnew[x,y][1]
            magz = spinsnew[x,y][2]

            pinning = deffects[x,y]
                
            if (pinning[0] == 0):
                magx = 0
                magy = 0
                magz = 0
            
            denominator = np.sqrt(magx**2 + magy**2 + magz**2)

            if (denominator != 0):
                spinsnew[x,y][0] = magx / denominator
                spinsnew[x,y][1] = magy / denominator
                spinsnew[x,y][2] = magz / denominator
            else:
                spinsnew[x,y][0] = 0
                spinsnew[x,y][1] = 0
                spinsnew[x,y][2] = 0
            
            energy1 = calcHam(spins)

            dE = energy1 - energy0

            if dE < 0 or random.random() < exp(-dE/T):
                spins = np.copy(spinsnew)
                energies.append(energy1)
                energy0 = energy1

            if energy1 <= Emin:
                Emin = energy1
                spinsmin = np.copy(spinsnew)
        
        T = dec * T
        
        print(f"MT - Temp: {T:5f}\tEmin: {Emin:5f}")
        
        if (step % 10000 == 0 and step > 0):    
            plot.spins2DT(spinsmin, step)

    return spinsmin

#@todo: normalization
def sa(spins):
    decrement = 0.9
    currentTemp = 20.0
    loop = True
    Emin = calcHam(spins)
    spinsmin = np.copy(spins)
    spinsnew = np.copy(spins)
    energy0 = calcHam(spins)
    print(f"SA - Starting Energy: {Emin:5f}")

    while loop:    
        for step in range(params.n):                
            spinsnew = np.copy(lattice.kick(np.copy(spins), currentTemp))

            energy1 = calcHam(spinsnew)

            dE = energy1 - energy0

            if dE < 0 or random.random() < exp(-dE/currentTemp):
                spins = np.copy(spinsnew)
                energy0 = energy1
            
            if energy1 < Emin:
                Emin = energy1
                spinsmin = np.copy(spinsnew)
            
        currentTemp = decrement * currentTemp

        print(f'SA - Temp: {currentTemp:5f}\tEmin: {Emin:5f}')
        
        if (currentTemp < 0.02):
            loop = False
        
    return spinsmin

def hamiltonian(spinLattice, i, j):
    Hex = np.copy(scalarExchange(spinLattice, i, j)) / 2.0
    Hz = np.copy(scalarZeeman(spinLattice, i, j))
    Hdm = np.copy(scalarDm(spinLattice, i, j)) / 2.0
	
    return Hex + Hdm + Hz

def scalarZeeman(spinLattice, i, j):
    return -np.dot(params.H, spinLattice[i,j])	

def scalarExchange(spinLattice, i, j):
	s = 0.0
	for i_ in range(-1, 2):
		if(i_ == 0): continue
		iint = i + i_
		if iint >= params.Nx: iint = 0
		elif iint < 0: iint = params.Nx - 1
		s += np.dot(spinLattice[i][j], spinLattice[iint][j])

	for j_ in range(-1, 2):
		if(j_ == 0): continue
		jint = j + j_
		if jint >= params.Ny: jint = 0
		elif jint < 0: jint = params.Ny - 1
		s += np.dot(spinLattice[i][j], spinLattice[i][jint])

	return -params.J * s / 2.0
	
def scalarDm(spinLattice, i, j):
	xdir = [1,0,0]
	ydir = [0,1,0]
	tempx = np.cross(spinLattice[i][j], spinLattice[i][j])

	for i_ in range(-1, 2):
		if(i_ == 0): continue
		iint = i + i_
		if iint >= params.Nx: iint = 0
		elif iint < 0: iint = params.Nx - 1
		tempx += np.cross(spinLattice[i][j], spinLattice[iint][j] * i_ / abs(i_))
	tempx = np.dot(tempx, xdir)

	tempy = np.cross(spinLattice[i][j], spinLattice[i][j])
	for j_ in range(-1, 2):
		if(j_ == 0): continue
		jint = j + j_
		if jint >= params.Ny: jint = 0
		elif jint < 0: jint = params.Ny - 1
		tempy += np.cross(spinLattice[i][j], spinLattice[i][jint] * j_ / abs(j_))
	tempy = np.dot(tempy, ydir)

	return -params.D * (tempx + tempy)