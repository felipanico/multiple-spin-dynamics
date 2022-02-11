import numpy as np
import plot
import lattice
import calc
import params
import monte_carlo
import sys

# Parameters
n = params.n
h = params.h
Nx = params.Nx
Ny = params.Ny

np.random.seed(0)

if (params.readDeffects):
    deffects = lattice.readDeffects()
else:
    deffects = lattice.createDeffects()

if (params.random):
    spins = lattice.createSpinLattice()
else:
    spins = lattice.readSpinLattice(params.inputFile)

spins = np.copy(lattice.normalization(spins, deffects))

plot.spins2DT(spins, 1)

if (params.minimize):
    #Monte Carlo
    spins = np.copy(monte_carlo.metropolis(spins, deffects))
else:    
    #LLG
    finalSpins = np.zeros((params.Nx, params.Ny,3))
    for step in range(n + 1):
        spins = np.copy(calc.llgEvolve(spins, finalSpins))
        spins = np.copy(lattice.normalization(spins, deffects))
        
        if (step % params.outputInterval == 0 and step > 0):    
            print('LLG step:', step)        
            plot.spins2DT(spins, step)
