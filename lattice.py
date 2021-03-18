import numpy as np

def createSpinLattice(n,Nx,Ny,mx,my,mz):
    spinLattice = np.zeros((Nx+2,Ny+2,3),np.float64)[1:Nx+1,1:Ny+1,:]
    
    for v in range(n-1):
        u = 0
        for x in range(Nx):
            for y in range(Ny):
                z = x + y
                spin = [x + 1, y + 1, z + 1]
                spinLattice[x][y] = spin
                
                mx[u][v] = spin[0]
                my[u][v] = spin[1]
                mz[u][v] = spin[2]
                
                u = u+1
    
    return spinLattice