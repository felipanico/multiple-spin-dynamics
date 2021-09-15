from hashlib import new
from typing import final
from plot import oldSpins2D
import random
import math
import calc
import sys
import params
from math import exp
import numpy as np
import lattice

def metropolis(spins):
    energy = 0
    energies = []
    T = 10
    T2 = 0.00001
    dec = 0.9

    while (T > T2):
        for step in range(params.n):
            for i in range(params.Nx):
                for j in range(params.Ny):
                    energy1 = calc.hamiltonian(spins, i, j)
                    oldSpin = spins[i,j]

                    x = np.random.randint(0, params.Nx + 1)
                    y = np.random.randint(0, params.Ny + 1)
                    
                    spins[x,y][0] = np.copy(spins[x,y][0]) + math.sqrt(T)*(random.random() - 0.5)
                    spins[x,y][1] = np.copy(spins[x,y][1]) + math.sqrt(T)*(random.random() - 0.5) 
                    spins[x,y][2] = np.copy(spins[x,y][2]) + math.sqrt(T)*(random.random() - 0.5)

                    magx = spins[x,y][0]
                    magy = spins[x,y][1]
                    magz = spins[x,y][2]

                    spins[x,y][0] = magx / np.sqrt(magx**2 + magy**2 + magz**2)
                    spins[x,y][1] = magy / np.sqrt(magx**2 + magy**2 + magz**2)
                    spins[x,y][2] = magz / np.sqrt(magx**2 + magy**2 + magz**2)
                    
                    energy2 = calc.hamiltonian(spins, i, j)

                    dE = energy1 - energy2

                    if dE < 0 or random.random() < exp(-dE/T):
                        spins[x,y] = oldSpin
                        energy += dE
                        energies.append(energy)
        T = dec * T
        print('current temp', T)

    return spins

def sa(spins):
    decrement = 0.9
    currentTemp = 10
    loop = True
    
    while loop:    
        for step in range(params.n):    
            energy0 = 0
            for i in range(params.Nx):
                for j in range(params.Ny):
                    energy0 += calc.hamiltonian(spins, i, j)
            
            newSpins = np.copy(lattice.kick(spins, currentTemp))

            energy1 = 0
            for x in range(params.Nx):
                for y in range(params.Ny):
                    energy1 += calc.hamiltonian(newSpins, x, y)

            dE = energy1 - energy0

            if dE < 0 or random.random() < exp(-dE/currentTemp):
                spins = np.copy(newSpins)
            
        currentTemp = decrement * currentTemp

        print('current temp', currentTemp)
        
        if (currentTemp < 0.00001):
            loop = False
        
    return spins