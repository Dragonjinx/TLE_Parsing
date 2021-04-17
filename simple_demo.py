import orbit_classes as oc
from TLE_parser import TLE , TLE_From_File
import random


if __name__ == '__main__':

    time_frame = 3000 # seconds
    time_step = 60 # seconds
    
    states = []

    # for i in range(5):
    #     height = random.randint(1, 100) * 100
    #     x = random.randint(1, 10) * 100
    #     y = random.randint(1, 10) * 100
    #     z = random.randint(1, 10) * 100
    #     vx = random.randint(1, 5)
    #     vy = random.randint(1, 5)
    #     vz = random.randint(1, 5)
    #     st = oc.State(height, x, y, z, vx, vy, vz)
    #     print(st.get_elements())
    #     states.append(st)

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

