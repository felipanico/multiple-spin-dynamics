import numpy as np

#loop
n = 1000
h = 0.02

#spins
spinsNumber = 3
Nx = 3
Ny = 1
spinsTotal = Nx * Ny

J = 1 #mev
Ms = 1 #saturation magnetisation (?)
D = 1
B = 0

alpha = 1 #program micro llg
gamma = 3.5 #program micro llg

H = np.array([0,0,B])
