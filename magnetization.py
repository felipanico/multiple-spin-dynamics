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
spins = lattice.createSpinLattice()

#@TODO LIST
# 1. read spins from file
# 2. plot readed spins
# 3. fix boundary conditions
# 4. add spin transfer torque
# 5. move skyrmion

if (params.minimize):
    #Monte Carlo
    spins = np.copy(monte_carlo.metropolis(spins))
else:    
    #LLG
    finalSpins = np.zeros((params.Nx + 2,params.Ny + 2,3))
    for step in range(n):
        spins = np.copy(lattice.createPbc(spins))
        spins = np.copy(calc.llgEvolve(spins, finalSpins))
        spins = np.copy(lattice.normalization(spins))        

    spins = np.copy(lattice.createPbc(spins))

plot.spins2DT(spins)
