from hashlib import new
from typing import final
import random
import math
import calc
import params
from math import exp
import numpy as np
import lattice

def calcHam(spins):
    H = 0.0
    for i in range(params.Nx):
        for j in range(params.Ny):
            H += calc.hamiltonian(spins, i, j)
    return H


def metropolis(spins):
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

            spinsnew[x,y][0] = magx / np.sqrt(magx**2 + magy**2 + magz**2)
            spinsnew[x,y][1] = magy / np.sqrt(magx**2 + magy**2 + magz**2)
            spinsnew[x,y][2] = magz / np.sqrt(magx**2 + magy**2 + magz**2)
            
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

    return spinsmin

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