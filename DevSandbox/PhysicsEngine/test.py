import engine_rev2 as e
import matplotlib.pyplot as plt
from math import sqrt



steps = 10
deltat = 0.01



bh = e.object(0,0,0,0,10**10)

vel = 0.05


projs = [
   # e.object(7, 0, 0, -0.043, 10**4, 0.05),
    e.object(7, 0, 0, vel+0.001, 10**5, 0.05),
    e.object(7, 0, 0, -vel, 10**4, 0.05),
]



# ! for 1 run only
# (projectiles, deltat) = e.nbody_coupled_integrator(projs, bh, steps, deltat)
# fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
# circle = plt.Circle((0, 0), 1, transform=ax.transData._b, color="red", alpha=0.4)
# ax.add_artist(circle)

# for proj in projectiles:

#     theta = proj.theta_list
#     r = proj.r_list

#     ax.plot(theta, r)
#     # ax.plot(theta, r, linestyle="", marker="o")





# ! for multiple runs
projectiles = projs

inp = ""

while inp == "":

    projs = list(projectiles)

    (projectiles, deltat) = e.nbody_coupled_integrator(projs, bh, steps, deltat)

    plt.close()

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    circle = plt.Circle((0, 0), 1, transform=ax.transData._b, color="red", alpha=0.4)
    ax.add_artist(circle)

    for proj in projectiles:

        theta = proj.theta_list
        r = proj.r_list


        ax.plot(theta, r)
        # ax.plot(theta, r, linestyle="", marker="o")

    #reset objects
    projs = list([])
    to_rm = []
    for p in projectiles:
        if p.IsOut: to_rm.append(p); pass
        p.UpdateVariables(deltat)
        projs.append(  e.object(p.r, 
                                p.theta,
                                p.vr,
                                p.vtheta,
                                p.m,
                                p.radius)    )
    projectiles = [p for p in projs]
    for p in to_rm:
        projectiles.remove(p)



    if projectiles == []:
        plt.show()
        plt.pause(0.001)
        input("system has finished simulation, no objects reamining. ")
        quit()

    plt.draw()
    plt.pause(0.001)

    inp = input("enter to continue > ")


