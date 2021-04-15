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

    for stt in states:
        satel = oc.Satellite(stt, 30, 60)
        saat.append(satel)

    # sat_state1 = oc.State(2000)
    # sat_state2 = oc.State(5000)
    # Sat = oc.Satellite(sat_state1, 30, 60)
    # Sat2 = oc.Satellite(sat_state2, 30, 60)
    # Sat.animate_sat_orb()
    # Sat2.animate_sat_orb()
    # plot_orbits([Sat, Sat2])
    # saat = [Sat, Sat2]
    anime = oc.animate_orbits(saat, factor=10)
    # anime.save("single.gif", writer='imagemagick', fps=60)