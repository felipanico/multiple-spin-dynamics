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
stepFileName = params.initialStep

#np.random.seed(0)

if (params.pinningDensity > 0): 
    lattice.createDeffectsAsFile()
    sys.exit()

if (params.useDeffects):
    deffects = lattice.chooseDeffects()
else:
    deffects = np.zeros((params.Nx,params.Ny,3), np.float64)

if (params.random):
    spins = lattice.createSpinLattice()
elif (params.createSkyrmion): 
    spins = np.copy(lattice.iniSkyrmionMumax())
else:
    spins = lattice.readSpinLattice(params.inputFile)

spins = np.copy(lattice.normalization(spins, deffects))

if (params.createFerromagnetic): 
    spins = np.copy(lattice.iniFerromagnetic())

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
            stepFileName = stepFileName + step
            print('LLG step:', stepFileName)        
            plot.spins2DT(spins, stepFileName)

if (params.saveLattice): 
    print("Saving Lattice...")
    lattice.writeSpinLattice(spins, "output/spins.in", np.float64)

if (params.saveDeffects): 
    print("Saving Deffects...")
    lattice.writeSpinLattice(deffects, "output/vac.in", np.int0)

print("End of execution")
