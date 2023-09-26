import engine as e
import matplotlib.pyplot as plt


steps = 100000
deltat = 0.01



bh = e.object(0,0,0,0,10**10)

proj = e.object(10, 0, 0, 0.02225, 10**4)

#for proj
l0_proj = e.compute_l0(proj.r, proj.vtheta)



proj1 = e.object(10, 0, 0, 0.02225, 10**4)
proj2 = e.object(10, 0, -0.2, 0.02225, 10**4)




# ! was test 1, non coupled integrator, needs to be coupled for
# ! deltat to be dynamic
"""
theta = [0]
r = []


#leapfrog returns all r already
r = e.Leapfrog_integrator(proj, bh, steps, l0_proj, deltat)[0]

#needs to compute all theta using v[]
for val in r:
    theta.append( e.theta_next(theta[-1], l0_proj, val, deltat) )

"""




#test using coupled integrators for 1 object
values = e.coupled_integrator(proj, bh, steps, l0_proj, deltat)

theta = values[1]
r = values[0]


"""

"""










fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

circle = plt.Circle((0, 0), 1, transform=ax.transData._b, color="red", alpha=0.4)
ax.add_artist(circle)

ax.plot(theta, r)
plt.show()



