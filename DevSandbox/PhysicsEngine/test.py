import engine as e
import matplotlib.pyplot as plt







steps = 100000
deltat = 0.01




class object:
    def __init__(self, r, theta, vr, vtheta, m):
        self.r = r
        self.theta= theta
        self.vr = vr
        self.vtheta= vtheta
        self.m = m
    
    def speed(self):
        return (self.vr, self.vtheta)

    def position(self):
        return (self.r, self.theta)
    


bh = object(0,0,0,0,10**10)

proj = object(5, 0, 0, 0.1, 1000)


#for proj
l0_proj = e.compute_l0(proj.r, proj.vtheta)
















theta = [0]
r = []


#leapfrog returns all r already
r = e.Leapfrog_integrator(proj, bh, steps, l0_proj, deltat)[0]

#needs to compute all theta using v[]
for val in r:
    theta.append( e.theta_next(theta[-1], l0_proj, val, deltat) )






fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(theta[10:], r[9:])
plt.show()




