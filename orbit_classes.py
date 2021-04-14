import numpy as np
import matplotlib as plt
from scipy.integrate import ode
import differentail_solver as ds

import planetary_data as pd

class State:
    def __init__(self, orbit_height = 0, x = 0, y = 0, z = 0, vx = 0, vy = 0, vz = 0):
        self.orbit_height = orbit_height
        self.initial_pos = [x, y, z]
        self.initial_vel = [vx, vy, vz]
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
    def update_pos(self, new_pos):
        self.x = new_pos[0]
        self.y = new_pos[1]
        self.z = new_pos[2]
    def update_vel(self, new_vel):
        self.vx = new_vel[0]
        self.vy = new_vel[1]
        self.vz = new_vel[2]


class Satellite:
    def __init__(self, state, period, dt, orbit_body=pd.earth):
        self.state = state
        self.period = period
        self.dt = dt
        self.orbit_body = orbit_body

    def propagate_orbit(self):
        #Radius of orbit
        r_mag = self.orbit_body['radius'] + self.state.orbit_height
        #Speed
        v_mag = np.sqrt(self.orbit_body['Mu'] / r_mag)
        #Period
        per = np.sqrt( ( r_mag**3 * 4 * np.pi** 2) / self.orbit_body['Mu'])
        if self.period > per:
            per = self.period
        
        #Timestep 
        
        #Number of steps
        steps = int(np.ceil(per/self.dt))
        
        #Set initial conditions
        self.state.update_pos([r_mag, 0, 0])
        self.state.update_vel([0, v_mag, 0])

        r0 = np.array([r_mag, 0,0])
        v0 = np.array([0, v_mag, 0])


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
        solver.set_f_params(self.orbit_body['Mu'])

        while solver.successful() and step < steps:
            solver.integrate(solver.t+self.dt)
            ts[step] = solver.t
            ys[step] = solver.y
            self.state.update_pos(solver.y[:3])
            self.state.update_vel(solver.y[3:6])
            step+=1
        rs = ys[:,:]
        ds.plot_animate(rs, self.orbit_body['radius'], steps, self.dt)


if __name__ == '__main__':
    sat_state = State(2000)
    Sat = Satellite(sat_state, 500, 60)
    Sat.propagate_orbit()