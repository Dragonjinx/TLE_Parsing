import numpy as np
from numpy import linalg
from scipy.integrate import ode
import plotter
import differentail_solver as ds
import planetary_data as pd

#Distace is in Km and velocity is in Km/s
class State:
    def __init__(self, orbit_height = 0, x = 0, y = 0, z = 0, vx = 0, vy = 0, vz = 0):
        self.orbit_height = orbit_height #Km
        self.initial_pos = [x, y, z]
        self.initial_vel = [vx, vy, vz]
        self.x = x # Km
        self.y = y # Km
        self.z = z # Km
        self.vx = vx #Km/s
        self.vy = vy #Km/s
        self.vz = vz #Km/s
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
    def __init__(self, state, period, dt, central_body=pd.earth, complete=True):
        self.state = state
        self.period = period
        self.dt = dt
        self.central_body = central_body
        self.FullAnimation = complete
        
        # Radios of orbit
        self.r_mag = self.central_body['radius'] + self.state.orbit_height #Km

        # Keplar's Laws:
        # Tangential speed required to maintain a circular obit
        self.min_v_mag = np.sqrt(self.central_body['Mu'] / self.r_mag) # KM / s
        # Period of a circular orbit with minimum velocity
        per = np.sqrt( ( self.r_mag**3 * 4 * np.pi** 2) / self.central_body['Mu']) # s
        
        #Check to set animation period
        if self.period > per and self.FullAnimation == True:
            per = self.period
        elif self.FullAnimation == False:
            per = self.period
        #Number of steps
        self.steps = int(np.ceil(per/self.dt))
        #Set initial conditions if none are given:
        if linalg.norm(self.state.get_elements()) == 0:
            self.state.update_pos([self.r_mag, 0, 0])
            self.state.update_vel([0, self.min_v_mag, 0])
        elif linalg.norm(self.state.get_pos()) < self.r_mag:
            self.state.update_pos([self.r_mag, 0, 0])

        #Update initial positions
        self.state.initial_pos = list(self.state.get_pos())
        self.state.initial_vel = list(self.state.get_vel()) 
    
    def propagate_orbit(self, reset=False):

        if reset == True:
            #Reset to initial values 
            self.state.update_pos(self.state.initial_pos)
            self.state.update_vel(self.state.initial_vel)

        y0 = self.state.get_elements()

        #initialize orbit and timestep array (efficiency)
        ys = np.zeros((self.steps, 6))
        ts = np.zeros((self.steps, 1)) 

        #initial state:
        ys[0] = y0
        step = 1

        #define the differentail solver
        solver = ode(ds.differential)
        solver.set_integrator('lsoda')
        solver.set_initial_value(y0, 0)
        solver.set_f_params(self.central_body['Mu'])

        #Solve position and velocity for the orbit period
        while solver.successful() and step < self.steps:
            # Stop if it hits earth:
            if linalg.norm(self.state.get_pos()) < self.central_body['radius']:
                ts[step] = solver.t
                ys[step] = self.state.get_elements()
                step +=1
            else:
                solver.integrate(solver.t+self.dt)
                self.state.update_pos(solver.y[:3])
                self.state.update_vel(solver.y[3:6])
                ts[step] = solver.t
                ys[step] = solver.y
                step+=1
        #Store all position 
        rs = ys[:self.steps,:]
        self.time_per_frame = str(self.dt) + ' seconds'
        return rs
    
    def plot_sat_orb(self):
        plotter.plot_n(self.propagate_orbit(), self.central_body['radius'])

    def animate_sat_orb(self):
        plotter.plot_animate(self.propagate_orbit(), self.central_body['radius'], self.steps, self.dt)

def max_steps(*Satellites):
    # Input handling
    for i in range(len(Satellites)):
        a = tuple(Satellites[i])
        Satellites = Satellites[:i] + a + Satellites[i+1:]

    max_stp = 0
    for i in Satellites:
        if i.steps > max_stp:
            max_stp = i.steps
    return max_stp

def animate_orbits(Satellites, factor = 1, override=False):
    # Number of orbits to animate
    orbits = len(Satellites)
    rs = [None] * orbits
    orb = 0
    animation_steps = max_steps(Satellites) * factor
    print('Frames:', animation_steps)
    print('Duration (s):' , (Satellites[0].dt * animation_steps * 0.01))
    for sat in Satellites:
        sat.steps = animation_steps
        rs[orb] = sat.propagate_orbit(reset=override)
        orb+=1
    
    if override == True:
        anime = plotter.plot_animate_n(rs, Satellites[0].central_body['radius'], 200 , Satellites[0].dt, orbits=orbits, show=False)
    else:
        anime = plotter.plot_animate_n(rs, Satellites[0].central_body['radius'], animation_steps , Satellites[0].dt, orbits=orbits, show=True)
    return anime

def plot_orbits(Satellites):
    # Number of orbits to animate
    orbits = len(Satellites)
    rs = [None] * orbits
    orb = 0
    for sat in Satellites:
        rs[orb] = sat.propagate_orbit()
        orb+=1
    
    # Satellites[0].steps
    plotter.plot_n(rs, Satellites[0].central_body['radius'])
    # return anime

def save_plot(Name, *Satellites):
    anime = animate_orbits(*Satellites, override=True)
    anime.save(Name + '.gif', writer='imagemagick', fps=60, progress_callback= lambda i, n: print(f'Saving frame {i} of {n}'))