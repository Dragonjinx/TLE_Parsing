import plotter
import numpy as np
from scipy.integrate import ode
import differentail_solver as ds

earth_radius = 6860
earth_Mu = 398600


if __name__ == '__main__':

    #Implementation of keplar's laws
    #Radius of orbit
    r_mag = earth_radius + 3000
    #Speed required to stay in a circular orbit of radius r_mag around the center of the earth
    v_mag = np.sqrt(earth_Mu / r_mag)
    #Period for the circular orbit
    per = np.sqrt( ( r_mag**3 * 4 * np.pi** 2) / earth_Mu ) * 10
    #Timestep 
    dt = 60
    #Number of steps
    steps = int(np.ceil(per/dt))
    
    #Set initial conditions
    r0 = np.array([r_mag,0,0])
    v0 = np.array([v_mag / 2, v_mag * 1.004, v_mag / 10])


    #initialize array (efficiency)
    ys = np.zeros((steps, 6))
    ts = np.zeros((steps, 1)) 

    #initial state:
    y0 = np.concatenate((r0, v0), axis=None)
    ys[0] = y0
    step = 1

    #define the differentail solver

    solver = ode(ds.differential)
    solver.set_integrator('lsoda')
    solver.set_initial_value(y0, 0)
    solver.set_f_params(earth_Mu)

    while solver.successful() and step < steps:
        solver.integrate(solver.t+dt)
        ts[step] = solver.t
        ys[step] = solver.y
        step+=1
    
    rs = ys[:, :]
    plotter.plot(rs, earth_radius)
    plotter.plot_animate(rs, earth_radius, steps, dt)