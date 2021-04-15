import orbit_classes as oc
import random

if __name__ == '__main__':

    states = []

    for i in range(5):
        height = random.randint(1, 100) * 100
        x = random.randint(1, 10) * 100
        y = random.randint(1, 10) * 100
        z = random.randint(1, 10) * 100
        vx = random.randint(1, 5)
        vy = random.randint(1, 5)
        vz = random.randint(1, 5)
        st = oc.State(height, x, y, z, vx, vy, vz)
        states.append(st)

    saat = []

    for stt in states   :
        satel = oc.Satellite(stt, 30, 60)
        saat.append(satel)

    # sat_state1 = oc.State(2000)
    # sat_state2 = oc.State(2000, 1000, 1000, 1000)
    # Sat1 = oc.Satellite(sat_state1, 30, 60)
    # Sat2 = oc.Satellite(sat_state2, 30, 60)
    # saat = [Sat1, Sat2]
    anime = oc.animate_orbits(saat, factor=10)
    # Uncomment at your own risk! 
    # anime.save("try.gif", writer='imagemagick', fps=60, progress_callback= lambda i, n: print(f'Saving frame {i} of {n}'))