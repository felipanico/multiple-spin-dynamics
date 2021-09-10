from hashlib import new
import random
import math
import calc
import sys
import params
from math import exp
from random import random
import numpy as np
import lattice

T = 0.5

def metropolis(spins):
    energy = 0
    energies = []
    
    for step in range(params.n):
        for i in range(params.Nx):
            for j in range(params.Ny):
                energy1 = calc.hamiltonian(spins, i, j)
                oldSpin = spins[i,j]

                i = np.random.randint(0, params.Nx + 1)
                j = np.random.randint(0, params.Ny + 1)
                energy2 = calc.hamiltonian(spins, i, j)

                dE = energy2 - energy1

                if dE < 0 or random() < exp(-dE/T):
                    spins[i,j] = oldSpin
                    energy += dE
                    energies.append(energy)

    return spins,energies

def sa(spins):
    currentTemp = 50
    finalTemp = .1
    decrement = 0.01
    
    energy = 0
    energies = []

    while currentTemp > finalTemp:
        print('current temp: ', currentTemp)
        for i in range(params.Nx):
            for j in range(params.Ny):
                spins, energy = calcEnergiesForSa(spins, i, j, energy, currentTemp)
                energies.append(energy)
        
        currentTemp -= decrement

    return spins,energies

def calcEnergiesForSa(spins, i, j, energy, T):
    energy1 = calc.hamiltonian(spins, i, j)
    oldSpin = spins[i,j]

    i = np.random.randint(0, params.Nx + 1)
    j = np.random.randint(0, params.Ny + 1)
    energy2 = calc.hamiltonian(spins, i, j)

    dE = energy2 - energy1

    if dE < 0 or random() < exp(-dE/T):
        spins[i,j] = oldSpin
        energy += dE
    
    return spins, energy