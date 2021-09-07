from hashlib import new
import random
import math
import calc
import sys
import params
from math import exp
from random import random
import numpy as np
import lattice

T = 1

def metropolis(spins):
    energy = 0
    energies = []

    for step in range(params.n):
        for i in range(params.Nx):
            for j in range(params.Ny):
                spins = np.copy(lattice.normalization(spins))
                spins = np.copy(lattice.createPbc(spins))
                dE = calc.hamiltonian(spins, i, j)
                
                if dE < 0 or random() < exp(-dE/T):
                    spins[i,j] = calc.vetorialExchange(spins, i, j)
                    energy += dE
                    energies.append(energy)

    return spins,energies

#T próximo 0
#L chegando ao fim

def sa(initial_state):
    """Peforms simulated annealing to find a solution"""
    initial_temp = 90
    final_temp = .1
    alpha = 0.01
    
    current_temp = initial_temp

    # Start by initializing the current state with the initial state
    current_state = initial_state
    solution = current_state

    while current_temp > final_temp:
        neighbor = random.choice(get_neighbors())

        # Check if neighbor is best so far
        cost_diff = get_cost(current_state) - get_cost(neighbor)

        # if the new solution is better, accept it
        if cost_diff > 0:
            solution = neighbor
        # if the new solution is not better, accept it with a probability of e^(-cost/temp)
        else:
            if random.uniform(0, 1) < math.exp(-cost_diff / current_temp):
                solution = neighbor
        # decrement the temperature
        current_temp -= alpha

    return solution

def get_cost(state):
    """Calculates cost of the argument state for your solution."""
    raise NotImplementedError
    
def get_neighbors(state):
    """Returns neighbors of the argument state for your solution."""
    raise NotImplementedError