# Classical Keplerian orbital elements:

# Epoch: Describes the time at which these elements were taken

# Shape of orbits;
# ECCENTRICITY => Defines how the orbit ellipse looks compared to a circle. Between 0 and 1
# SEMIMAJOR AXIS =? Line between periapsis and aposapsis

# Orbital plane:
# LONGITUDE OF ASCENDING NODE / RIGHT ASCENSION OF ASCENDING NODE => Angle between reference point and ASCENDING NODE 
# INCLINATION: Angle of the orbital plane compared to equator at ASCENDING NODE

# Positioning:
# ARGUMENT OF PERIAPSIS => Angle between PERIAPSIS and ASCENDING NODE
# TRUE ANOMALY => Angle between PERIAPSIS and position of the satellite in orbit at the EPOCH


# Two line elements:
# Eccentricity
# Inclination
# Longitude of ascending node
# Argument of periapsis
# Mean motion 
# Mean anomaly


# Perifocal Frame:
# Frame of reference where X axis is pointed to the periapsis and z axis is parallel to the angular momentum

from math import cos, sin, sqrt
import numpy as np

from spiceypy import oscltx, conics
# Thank you people at nasa for doing a much more efficient implementation of this.
# conics => Gives state vector from orbital elements
# conics documentation: https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/conics_c.html
# oscltx => Gives orbital parameters from state vector
# ocltx documentation: https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/oscltx_c.html
# NASA CSPICE toolkit Documentation: https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/index.html
# scpicepy wrapper documentation: https://spiceypy.readthedocs.io/en/main/index.html
import planetary_data as pd
from orbit_classes import State

deg_to_rad = np.pi / 180

class TLE:
    def __init__(self, TwoLineElementString, central_body= pd.earth):
        self.TLE_STR = TwoLineElementString
        self.Central_body = central_body
        self.tle_to_data()
        self.tle_set_state()

    # Parse reference: https://en.wikipedia.org/wiki/Two-line_element_set
    def tle_to_data(self):

        Lines = self.TLE_STR.split('\n')

        line0 = Lines[0]
        line1 = Lines[1].split()
        line2 = Lines[2].split()
        
        # Parameters read from the TLE String
        self.Name = line0
        self.Epoch = float(line1[3]) 
        # Eccentricity is assumed to be a decimal
        self.Eccentricity = float('0.' + line2[4]) 
        self.Longitude_of_ascending_node = float(line2[3])
        self.Argument_of_periapsis = float(line2[5])
        self.Inclination = float(line2[2])
        self.Mean_motion = float(line2[7])
        self.Mean_anomaly = float(line2[6])
        self.Period = 1/self.Mean_motion * 24 * 3600 # Seconds
        
        # Parameters to calculate
        # self.True_anomaly = str_data[6]
        
        # Semimajor axis calculation reference: https://en.wikipedia.org/wiki/Semi-major_and_semi-minor_axes
        # Under Orbital Period 
        self.Semimajor_axis = np.cbrt((self.Period ** 2 * self.Central_body['Mu'] / (4.0 * np.pi**2)))
        # Apsis heights: https://en.wikipedia.org/wiki/Apsis
        self.Periapsis_height = (1-self.Eccentricity) * self.Semimajor_axis
        self.Apoapsis_height = (1+self.Eccentricity) * self.Semimajor_axis

    def tle_set_state(self):
        self.TLE_state = State(0)
        conics_input = [self.Periapsis_height, self.Eccentricity, self.Inclination,
                        self.Longitude_of_ascending_node, self.Argument_of_periapsis, self.Mean_anomaly,
                        self.Epoch, self.Central_body['Mu']]
        state_vector = conics(conics_input, 0)
        # self.TLE_state.orbit_height = self.Periapsis_height
        self.TLE_state.update_pos(state_vector[:3])
        self.TLE_state.update_vel(state_vector[3:])