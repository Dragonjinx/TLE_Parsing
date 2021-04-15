import orbit_classes as oc

if __name__ == '__main__':
    sat_state1 = oc.State(2000)
    sat_state2 = oc.State(5000)
    Sat = oc.Satellite(sat_state1, 30, 60)
    Sat2 = oc.Satellite(sat_state2, 30, 60)
    # Sat.animate_sat_orb()
    # Sat2.animate_sat_orb()
    # plot_orbits([Sat, Sat2])
    saat = [Sat, Sat2]
    anime = oc.animate_orbits(saat)
    # anime.save("single.gif", writer='imagemagick', fps=60)