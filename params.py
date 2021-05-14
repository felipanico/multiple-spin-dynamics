import numpy as np

#loop
n = 1000
h = 0.02

#spins
spinsNumber = 10
Nx = spinsNumber
Ny = spinsNumber
spinsTotal = Nx * Ny

J = 1 #mev
Ms = 1 #saturation magnetisation (?)
D = 0.18
B = 1

alpha = 0.02 #program micro llg
gamma = 3.5 #program micro llg

H = np.array([0,0,B])
