import numpy as np
import sys
import plot
import lattice
import calc

# Parameters for lower magnetic field
#n = 1000
#h = 0.05
#Nx = 2
#Ny = 2
#H = np.array([0,0,1])
#initialScale = 10
#finalScale = 5*10**(-6)

# Parameters for higher magnetic field
n = 3000
h = 0.01
Nx = 5
Ny = 5
H = np.array([0,0,10])
initialScale = 10
finalScale = 5*10**(-6)

# Create initial values and running calculation
mx = np.zeros((Nx*Ny,n-1))
my = np.zeros((Nx*Ny,n-1))
mz = np.zeros((Nx*Ny,n-1))

spinLattice = lattice.createSpinLattice(n,Nx,Ny,mx,my,mz)

spinTotal = Nx*Ny

plot.spins2D(spinLattice, initialScale, 0.1, 0.5)

for t in range(n-1):
	i = 0
	for x in range(Nx):
		for y in range(Ny):
			spin = calc.euler(spinLattice[x][y], spinLattice, H, spinTotal, t, mx, my, mz, h, x, y)
			mx[i][t] = spin[0]
			my[i][t] = spin[1]
			mz[i][t] = spin[2]
			i = i+1

print(spinLattice)
sys.exit()
plot.spins2D(spinLattice, finalScale, -1, 1)
plot.spins3D(t, spinTotal, mx, my, mz)

