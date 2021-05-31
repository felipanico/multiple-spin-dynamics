import numpy as np

#loop
n = 50000
h = 0.01

#spins
spinsNumber = 3
Nx = 20
Ny = 20
spinsTotal = Nx * Ny

J = 1 #mev
Ms = 1 #saturation magnetisation (?)
D = 0.18
B = 0

alpha = 0.2 #program micro llg
gamma = 3.5 #program micro llg

H = np.array([0,0,B])
