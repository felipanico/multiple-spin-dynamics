import lattice
import params

print('Creating pinning file...')

if (params.pinningDensity > 0): 
    lattice.createDeffectsAsFile()
    print('Pinnning file was created')
else:
    print('Pinning density must be greater than zero')