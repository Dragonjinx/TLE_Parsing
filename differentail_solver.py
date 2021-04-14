import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

"""
F = GM m / r^2
Mu = GM
F_SAT = Mu m / r^2 
"""

#Serves as a initialization function for the background
def plot_bckground(ax, rplot):
    #plot body to orbit
    _u,_v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    _x = rplot*np.cos(_u)*np.sin(_v)
    _y = rplot*np.sin(_u)*np.sin(_v)
    _z = rplot*np.cos(_v)
    ax.plot_surface(_x, _y, _z, cmap='Blues', zorder=0)

    #X, y z axes lines
    l= rplot *2
    x, y, z = [[0,0,0], [0,0,0], [0,0,0]]
    u, v, w = [[l,0, 0], [0,l,0], [0, 0, l]]
    ax.quiver(x, y, z, u, v, w, color='k')
    
    #setting the labels in the plot
    ax.set_xlabel('X (km)'); ax.set_ylabel('Y km'); ax.set_zlabel('Z km');
    ax.set_aspect('auto', anchor='C')

    return ax

def plot_orbit(ax, r):
    #Trajectory and starting point of satellite
    ax.plot(r[:,0], r[:,1], r[:,2], 'k--', label='trajectory', zorder=10)
    ax.plot([r[0,0]],[r[0, 1]], [r[0,2]],'ko', label='Starting Position', zorder=20)
    return ax


def orbit_anim(frame, ax, r, orb, pos):
    #Trajectory and current position implementation to animate the satellite
    # The implementation below was a bad way of doing this, resulted in conflicts during animation
    # orb = ax.plot(r[:frame+1, 0], r[:frame+1, 1], r[:frame+1, 2], 'k--', label='trajectory', zorder=10)
    # This plotted a steady line of current position, don't do this 
    # ax.plot(r[frame, 0], r[frame, 1], r[frame, 2], 'go', zorder=10)
    orb.set_data(r[:frame+1, 0], r[:frame+1, 1])
    orb.set_3d_properties(r[:frame+1, 2], 'z')    
    pos.set_data(r[frame, 0], r[frame, 1])
    pos.set_3d_properties(r[frame, 2], 'z')
    return orb, pos

def plot(r, bod_rad):
    #Setup plot environment
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    #Defining plot limits
    max_val = np.max(np.abs(r))
    ax.set_xlim([-max_val, max_val])
    ax.set_ylim([-max_val, max_val])
    ax.set_zlim([-max_val, max_val])
    
    #Plot the orbit
    ax = plot_orbit(ax, r)    
    
    #define the radius of body to orbit
    rplot = bod_rad
    #plot body to orbit
    ax = plot_bckground(ax, bod_rad)

    plt.legend()
    plt.show()


def plot_animate(r, bod_rad, steps, dt):
    #Setup plot environment
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    max_val = np.max(np.abs(r))
    ax.set_xlim([-max_val, max_val])
    ax.set_ylim([-max_val, max_val])
    ax.set_zlim([-max_val, max_val])

    #Plot background and body to orbit
    ax = plot_bckground(ax, bod_rad)
    #Setup initial position and current position
    ax.plot([r[0,0]],[r[0, 1]], [r[0,2]],'ko', label='Starting Position', zorder=20)
    orb, = ax.plot(r[0,0], r[0,1], r[0,2], 'k--', label='trajectory', zorder=10)
    pos, = ax.plot([r[0,0]],[r[0, 1]], [r[0,2]],'go', label='Current Position', zorder=10)
    
    #Animate trajectory
    anime = animation.FuncAnimation(fig,  orbit_anim, fargs=(ax, r, orb, pos,), frames=steps, interval=dt, blit=True)
    
    plt.legend()
    plt.show()


earth_radius= 6376
earth_Mu= 398600


def differential(time, state, Mu):

    #Decompose the state to the position and velocities
    rx, ry, rz, vx, vy, vz = state

    #Vector pointing to smaller mass from the center of Mu mass
    _pos = np.array([rx, ry, rz])
    #Norm of the vector
    _pos_norm = np.linalg.norm(_pos)

    # a = r .Mu / r^3
    # We multiply by vector first to get the component wise accelleration, and then divide by its scalar for the correct magnitude
    ax, ay, az = - _pos * Mu / _pos_norm**3

    return [vx, vy, vz, ax, ay, az]




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

    solver = ode(differential)
    solver.set_integrator('lsoda')
    solver.set_initial_value(y0, 0)
    solver.set_f_params(earth_Mu)

    while solver.successful() and step < steps:
        solver.integrate(solver.t+dt)
        ts[step] = solver.t
        ys[step] = solver.y
        step+=1
    
    rs = ys[:, :]
    plot(rs, earth_radius)
    plot_animate(rs, earth_radius, steps, dt)