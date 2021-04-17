import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation, artist
import copy

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

def plot_orbit(ax, r, index=''):
    #Trajectory and starting point of satellite
    ax.plot(r[:,0], r[:,1], r[:,2], '--', label='trajectory' + index , zorder=10)
    ax.plot([r[0,0]],[r[0, 1]], [r[0,2]],'o', label='Starting Position' + index, zorder=20)
    return ax

def orbit_anim(frame, r, artists, frame_counter=False):
    #Trajectory and current position implementation to animate the satellite
    # The implementation below was a bad way of doing this, resulted in conflicts during animation
    # orb = ax.plot(r[:frame+1, 0], r[:frame+1, 1], r[:frame+1, 2], 'k--', label='trajectory', zorder=10)
    # This plotted a steady line of current position, don't do this 
    # ax.plot(r[frame, 0], r[frame, 1], r[frame, 2], 'go', zorder=10)
    r_indx = 0
    if frame_counter is not False:
        for art in artists[:-1]:
            art[0].set_data(r[r_indx][:frame, 0], r[r_indx][:frame, 1])
            art[0].set_3d_properties(r[r_indx][:frame, 2], 'z')    
            art[1].set_data(r[r_indx][frame, 0], r[r_indx][frame, 1])
            art[1].set_3d_properties(r[r_indx][frame, 2], 'z')
            r_indx += 1

        artists[-1][0].label = 'Frame: ' +str(frame)
        
    else:
        for art in artists:
            art[0].set_data(r[r_indx][:frame, 0], r[r_indx][:frame, 1])
            art[0].set_3d_properties(r[r_indx][:frame, 2], 'z')    
            art[1].set_data(r[r_indx][frame, 0], r[r_indx][frame, 1])
            art[1].set_3d_properties(r[r_indx][frame, 2], 'z')
            r_indx += 1

    # plt.legend('Frames: ' + str(frame))
    return sum(artists, [])

def plot_n(r, bod_rad):
    rx = list(r)
    #Setup plot environment
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    #Defining plot limits
    max_val = np.max(np.abs(bod_rad * 3))
    ax.set_xlim([-max_val, max_val])
    ax.set_ylim([-max_val, max_val])
    ax.set_zlim([-max_val, max_val])
    
    #Plot the orbit
    for rxx in rx:
        ax = plot_orbit(ax, rxx, str(rx.index(rxx)))    
    #define the radius of body to orbit    
    rplot = bod_rad
    #plot body to orbit
    ax = plot_bckground(ax, bod_rad)

    plt.legend()
    plt.show()

def plot_animate_n(r, bod_rad, steps, dt, orbits=1, Repeat=False, show=True, label=True):
    # Force r to be a list (For single value cases)
    rx = list(r)
    #Setup plot environment
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    max_val = np.max(np.abs(bod_rad * 3))
    ax.set_xlim([-max_val, max_val])
    ax.set_ylim([-max_val, max_val])
    ax.set_zlim([-max_val, max_val])

    #Plot background and body to orbit
    ax = plot_bckground(ax, bod_rad)
    #Setup initial position and current position
    
    # Setup artist list 
    artists = []
    indx = 0
    for tr in rx:
        indxstr = str(indx)
        # ax.plot(tr[0,0],tr[0, 1], tr[0,2],'o', label=('Starting Position ' + indxstr), zorder=20)
        a = ax.plot(tr[0,0], tr[0,1], tr[0,2], '--', label=('trajectory' + indxstr), zorder=10)
        b = ax.plot(tr[0,0],tr[0, 1], tr[0,2],'o', label=('Current Position' + indxstr), zorder=10)
        artists.append(a + b)
        # Valuable lessons learned, python lists dont work like c++ lists, if you wanna add new  vlaues, pls just append them
        # Its inefficient timewise I know, but if I try to have a predefined matrix and copy into them, it just copies the references
        # and the next time, it overrides the reference values
        # What not to do:
        # artists[index] = a + b
        indx += 1

    #Set point to display label in legend:
    if label is True:
        c = ax.plot([], [], [], label = 'Frame: 0', zorder = 0)
        artists.append(c)

    #Animate trajectory
    anime =  animation.FuncAnimation(fig,  orbit_anim, fargs=(r, artists,label), frames=steps, interval=dt, blit=True, repeat=Repeat, save_count=100)
    
    if show == True:
        plt.legend()
        plt.show()
    
    return anime