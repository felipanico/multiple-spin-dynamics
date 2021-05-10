import numpy as np

#loop
n = 300
h = 0.02

#spins
spinsNumber = 15
Nx = spinsNumber
Ny = spinsNumber
spinsTotal = Nx * Ny

J = 1 #mev
Ms = 1 #saturation magnetisation (?)
D = 0.18
B = 0.015

alpha = 0.2 #program micro llg
gamma = 3.5 #program micro llg

_lambda = 1

H = np.array([0,0,B])
