import numpy as np

#loop
n = 100
h = 0.01

#spins
spinsNumber = 10
Nx = spinsNumber
Ny = spinsNumber
spinsTotal = Nx * Ny

J = 1 #mev
D = 0.18
B = 1

alpha = 0.04
gamma = 0

H = np.array([0,0,B])

minimize = True
