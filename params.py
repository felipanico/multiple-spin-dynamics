import numpy as np

#loop
n = 50000
h = 0.01

#spins
spinsNumber = 25
Nx = spinsNumber
Ny = spinsNumber
spinsTotal = Nx * Ny

J = 1 #mev
Ms = 1 #saturation magnetisation (?)
D = 0.18
B = 0

alpha = 0.04
gamma = 0

H = np.array([0,0,B])
