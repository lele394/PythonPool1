import engine_rev2 as e
import matplotlib.pyplot as plt
from math import sqrt



steps = 500000
deltat = 0.01



bh = e.object(0,0,0,0,10**10)

vel = 0.04


projs = [
   # e.object(7, 0, 0, -0.043, 10**4, 0.05),
    e.object(7, 0, 0, vel, 10**4, 0.05),
    e.object(7, 0, 0, -vel, 10**4, 0.05),
]



objects = e.nbody_coupled_integrator(projs, bh, steps, deltat)



# * creates plot and add the black hole
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
circle = plt.Circle((0, 0), 1, transform=ax.transData._b, color="red", alpha=0.4)
ax.add_artist(circle)



for object in objects:

    theta = object.theta_list
    r = object.r_list


    ax.plot(theta, r)
    # ax.plot(theta, r, linestyle="", marker="o")



plt.show()

