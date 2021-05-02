import numpy as np

#loop
n = 1000
h = 0.01

#spins
spinsNumber = 20
Nx = spinsNumber
Ny = spinsNumber
spinsTotal = Nx * Ny

J = 1 #mev
Ms = 1 #saturation magnetisation (?)
D = 0.18
B = 0

alpha = 0.04 #program micro llg
gamma = 3.5 #program micro llg

_lambda = 1

H = np.array([0,0,B])

print("magnetic field", H)
print("lambda", _lambda)
