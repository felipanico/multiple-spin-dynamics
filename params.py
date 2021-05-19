import numpy as np

n = 1000
h = 0.01

spinsNumber = 10
Nx = 1
Ny = 10
spinsTotal = Nx * Ny

J = 0 #mev
Ms = 1 #saturation magnetisation (?)
D = 1
B = 0

alpha = 1
gamma = 3.5

H = np.array([0,0,B])
