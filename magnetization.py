import numpy as np
import sys
import plot
import lattice
import calc
import params
import monte_carlo

# Parameters
n = params.n
h = params.h
Nx = params.Nx
Ny = params.Ny

np.random.seed(0)

#@TODO LIST
# 1. fix boundary conditions
# 2. add spin transfer torque
# 3. move skyrmion

if (params.random):
    spins = lattice.createSpinLattice()
else:
    spins = lattice.readSpinLattice('data/input20x20.dat')

plot.spins2DT(spins, 1)
sys.exit()

if (params.minimize):
    #Monte Carlo
    spins = np.copy(monte_carlo.metropolis(spins))
else:    
    #LLG
    finalSpins = np.zeros((params.Nx, params.Ny,3))
    for step in range(n):
        spins = np.copy(calc.llgEvolve(spins, finalSpins))
        spins = np.copy(lattice.normalization(spins))
        
        if (step % 100 == 0):    
            print('LLG step:', step)        
            plot.spins2DT(spins, step)

plot.spins2DT(spins, 1)
