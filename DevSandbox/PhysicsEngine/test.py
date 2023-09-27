import engine_rev2 as e
import matplotlib.pyplot as plt
from math import sqrt, radians



steps = 10
deltat = 0.01



bh = e.object(0,0,0,0,10**10)

vel = 0.05


projs = [
   # e.object(7, 0, 0, -0.043, 10**4, 0.05),
    e.object(7, 0, 0, vel+0.001, 10**5, 0.05),
    e.object(7, 0, 0, -vel, 10**4, 0.05),
    e.object(7, 0, 0, 1, 10**4, 0.05),
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





# & tryna draw a line here
def DrawVector(object, r, theta, plot, color="blue"):
    r = [object.r, object.r+r]
    theta = [object.theta, object.theta + theta]
    print(r, theta)
    plot.plot(theta, r, color=color)




# ! for multiple runs
projectiles = projs

inp = ""

#sets darck background
# plt.style.use('dark_background')

while inp != "q":

    projs = list(projectiles)

    (projectiles, deltat) = e.nbody_coupled_integrator(projs, bh, steps, deltat)

    plt.close()

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    circle = plt.Circle((0, 0), 1, transform=ax.transData._b, color="red", alpha=0.4)
    ax.add_artist(circle)

    
    
    tempo_coordinates = []
    
    for proj in projectiles:
        theta = proj.theta_list
        r = proj.r_list
        tempo_coordinates.append([list(theta), list(r)])


        ax.plot(theta, r)
        # ax.plot(theta, r, linestyle="", marker="o")

    #reset objects
    projs = list([])
    for p in projectiles:
        if p.IsOut: continue
        p.UpdateVariables(deltat)
        projs.append(  e.object(p.r, 
                                p.theta,
                                p.vr,
                                p.vtheta,
                                p.m,
                                p.radius)    )
    projectiles = list(projs)


    if projectiles == []:
        plt.show()
        plt.pause(0.001)
        input("system has finished simulation, no objects reamining. ")
        quit()

    plt.draw()
    plt.pause(0.001)

    inp = input("q to quit > ")









    # continue

    # * testing implementation of missile firing
    if inp == "l":

        inp = input("   vr vtheta type\n > ")
        to_add = []
        while inp != "c" or inp !="cancel":
            if inp == "c": break

            inp_split = [float(i) for i in inp.split(" ")]


            ship_id = 0
            ship = projectiles[ship_id]


            plt.close()
            fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
            circle = plt.Circle((0, 0), 1, transform=ax.transData._b, color="red", alpha=0.4)
            ax.add_artist(circle)

    

            for proj in tempo_coordinates:
                theta = proj[0]
                r = proj[1]
                ax.plot(theta, r)
            
            #draw r and theta vect base
            DrawVector(ship, 1, 0, ax, "red") #r
            DrawVector(ship, 0, radians(8), ax, "white") #theta

            #draw launch vector
            DrawVector(ship, inp_split[0]*100, radians(inp_split[1])*100, ax, "green")

            to_add = [inp_split[0], inp_split[1]]




            plt.draw()
            plt.pause(0.001)    
            inp = input("> ")
        

    if inp == "c":
        # * adds projectile, mass 10**2 and radius 0.02
        projectiles.append( e.object(ship.r, ship.theta, to_add[0], to_add[1], 10**2, 0.02)   )
            





