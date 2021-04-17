import orbit_classes as oc
from TLE_parser import TLE
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

    # saat = []

    # for stt in states:
    #     satel = oc.Satellite(stt, time_frame, time_step)
    #     saat.append(satel)
    st = '''ISS
1 25544U 98067A   21107.58244333  .00000946  00000-0  25412-4 0  9990
2 25544  51.6445 282.4828 0002680 236.8482 199.8666 15.48892929279202'''
    implement = TLE(st)

    sat_state1 = implement.TLE_state
    # sat_state2 = oc.State(2000, 1000, 1000, 1000)
    # Sat1 = oc.Satellite(sat_state1, 30, 60)
    Sat1 = oc.Satellite(implement, 30, 60, t_l_e=True)
    # Sat2 = oc.Satellite(sat_state2, 30, 60)
    # saat = [Sat1, Sat2]
    # oc.plot_orbits(saat)
    anime = oc.animate_orbits([Sat1], factor=10, Repeat=True)
    # oc.save_plot('Try2', saat)
    # Uncomment at your own risk! 