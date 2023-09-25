import engine as e
import matplotlib.pyplot as plt


steps = 100000
deltat = 0.1



bh = e.object(0,0,0,0,10**10)

proj = e.object(15, 0, 0, 0.011, 1000)


#for proj
l0_proj = e.compute_l0(proj.r, proj.vtheta)




theta = [0]
r = []


#leapfrog returns all r already
r = e.Leapfrog_integrator(proj, bh, steps, l0_proj, deltat)[0]

#needs to compute all theta using v[]
for val in r:
    theta.append( e.theta_next(theta[-1], l0_proj, val, deltat) )





"""
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(theta[:-1], r)
plt.show()
"""



