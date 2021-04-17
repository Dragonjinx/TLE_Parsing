import orbit_classes as oc
from TLE_parser import TLE , TLE_From_File
import random


if __name__ == '__main__':

    time_frame = 3000 # seconds
    time_step = 60 # seconds
    
    # states = []
    # Problematic velocity
    # Either: vy = 4 and vz < 4
    # Or: vz = 4 and vy < 4
    # stt = oc.State(1600, 7078, vx=3, vy=3, vz=4)
    # states.append(stt)
    # for i in states:
    #     satel = oc.Satellite(i, 1000, 60, complete=False)
    #     saat.append(satel)

    saat = []
    tleeeee = []

    tles = TLE_From_File('TLE.txt')
    for i in tles:
        t = TLE(i)
        tleeeee.append(t)

    for i in tleeeee:
        satel = oc.Satellite(i, 1000, 60, t_l_e=True, complete=False)
        saat.append(satel)
    
    anime = oc.animate_orbits(saat, factor=10, Repeat=True)
    # oc.save_plot('ISS', [Sat1])

