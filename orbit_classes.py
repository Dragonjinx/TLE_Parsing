import numpy as np
from numpy import linalg
from scipy.integrate import ode
import plotter
import differentail_solver as ds
import planetary_data as pd

#Distace is in Km and velocity is in Km/s
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
    def get_pos(self):
        return np.array([self.x, self.y, self.z])
    def get_vel(self):
        return np.array([self.vx, self.vy, self.vz])
    def get_elements(self):
        return np.array([self.x, self.y, self.z, self.vx, self.vy, self.vz])

class Satellite:
    # Satellite State Object, Time Period to render, Time Step, Orbiting Body Object, Animate Complete Orbit
    def __init__(self, state, period, dt, orbit_body=pd.earth, complete=True):
        self.state = state
        self.period = period
        self.dt = dt
        self.orbit_body = orbit_body
        self.FullAnimation = complete
    def propagate_orbit(self):
        #Radius of orbit
        self.r_mag = self.orbit_body['radius'] + self.state.orbit_height

        #Keplar's Laws:
        #Tangential speed required to maintain a circular obit
        self.min_v_mag = np.sqrt(self.orbit_body['Mu'] / self.r_mag)
        #Period of a circular orbit with minimum velocity
        per = np.sqrt( ( self.r_mag**3 * 4 * np.pi** 2) / self.orbit_body['Mu']) * 20
        
        #Check to set animation period
        if self.period > per and self.FullAnimation == True:
            per = self.period
        elif self.FullAnimation == False:
            per = self.period
        
        #Number of steps
        steps = int(np.ceil(per/self.dt))
        
        #Set initial conditions if none are given:
        if linalg.norm(self.state.get_elements()) == 0:
            self.state.update_pos([self.r_mag, 0, 0])
            self.state.update_vel([0, self.min_v_mag, 0])
        elif linalg.norm(self.state.get_pos()) < self.r_mag:
            self.state.update_pos([self.r_mag, 0, 0])

        # old implementation
        # r0 = self.state.get_pos() 
        # v0 = self.state.get_vel()
        # y0 = np.concatenate((r0, v0), axis=None)
        y0 = self.state.get_elements()

        #initialize orbit and timestep array (efficiency)
        ys = np.zeros((steps, 6))
        ts = np.zeros((steps, 1)) 

        #initial state:
        ys[0] = y0
        step = 1

        #define the differentail solver
        solver = ode(ds.differential)
        solver.set_integrator('lsoda')
        solver.set_initial_value(y0, 0)
        solver.set_f_params(self.orbit_body['Mu'])

        #Solve position and velocity for the orbit period
        while solver.successful() and step < steps:
            solver.integrate(solver.t+self.dt)
            self.state.update_pos(solver.y[:3])
            self.state.update_vel(solver.y[3:6])
            # Stop if it hits earth:
            if linalg.norm(self.state.get_pos()) < self.orbit_body['radius']:
                steps = step
            ts[step] = solver.t
            ys[step] = solver.y
            step+=1
        #Store all position and 
        rs = ys[:steps,:]
        plotter.plot_animate(rs, self.orbit_body['radius'], steps, self.dt)


if __name__ == '__main__':
    sat_state = State(2000)
    Sat = Satellite(sat_state, 3000, 60)
    Sat.propagate_orbit()