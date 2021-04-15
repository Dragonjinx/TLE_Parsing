import numpy as np

#Need to implement change in position based on an equation to make the satellite thrust capable

def differential(time, state, Mu):

    #Decompose the state to the position and velocities
    # State is taken as a list instead of a class to simplify usage with ode.integrate()
    rx, ry, rz, vx, vy, vz = state

    #Vector pointing to smaller mass from the center of Mu mass
    _pos = np.array([rx, ry, rz])
    #Norm of the vector
    _pos_norm = np.linalg.norm(_pos)

    # a = r .Mu / r^3
    # We multiply by vector first to get the component wise accelleration, and then divide by its scalar for the correct magnitude
    ax, ay, az = - _pos * Mu / _pos_norm**3

    return [vx, vy, vz, ax, ay, az]

