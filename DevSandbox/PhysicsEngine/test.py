import engine_rev2 as e
import matplotlib.pyplot as plt
from math import sqrt, radians

outOfBound = 5

steps = 1000
deltat = 0.01



bh = e.object(0,0,0,0,10**10)

vel = 0.04


projs = [
   # e.object(7, 0, 0, -0.043, 10**4, 0.05),
    e.object(7, 0, 0, vel, 10**4, 0.02),
    e.object(7, 0, 0, -vel, 10**4, 0.02),
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
    #sets boundaries
    ax.set_ylim([0,outOfBound])
    circle = plt.Circle((0, 0), 1, transform=ax.transData._b, color="red", alpha=0.4)
    ax.add_artist(circle)

    
    # * used as a temporary holder for below's POC
    tempo_coordinates = []
    
    for proj in projectiles:
        theta = proj.theta_list
        r = proj.r_list
        tempo_coordinates.append([list(theta), list(r)])


        ax.plot(theta, r)
        # ax.plot(theta[45:55], r[45:55], linestyle="-", marker="o")

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
        input("system has finished simulation, no objects reamining. Press enter to quit\n> ")
        quit()

    plt.draw()
    plt.pause(0.001)

    inp = input("q to quit > ")

    #set new steps and does a sim
    if "setsteps" in inp:
        steps = int(inp.split(" ")[-1])
        continue


    # ! comment to enable missile firing
    continue











    # * testing implementation of missile firing
    if inp == "l":

        inp = input("   vr vtheta type\n > ")
        to_add = [] # list to keep the coordinates of the new object
        while inp != "c" or inp !="cancel":
            if inp == "c": break

            # splicing?
            inp_split = [float(i) for i in inp.split(" ")]


            # ~ could just pass the ship object if we keep track of it above, add a "type" variables on objects?
            ship_id = 0
            ship = projectiles[ship_id]

            #need to close open windows before plotting again
            # ! might wanna change that, inneficient as FUCK and probably slowing this bitch down a lot
            plt.close()
            fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
            #sets boundaries
            ax.set_ylim([0,outOfBound])
            circle = plt.Circle((0, 0), 1, transform=ax.transData._b, color="red", alpha=0.4)
            ax.add_artist(circle)

    

            for proj in tempo_coordinates:
                theta = proj[0]
                r = proj[1]
                ax.plot(theta, r)
            
            #draw r and theta vect base
            DrawVector(ship, 1, 0, ax, "red") #r
            DrawVector(ship, 0, radians(8), ax, "white") #theta

            #draw launch vector, multiplied by 100 so we can see it, might wanna pass it in a log tho
            DrawVector(ship, inp_split[0]*100, radians(inp_split[1])*100, ax, "green")

            to_add = [inp_split[0], inp_split[1]]




            plt.draw()
            plt.pause(0.001)    
            inp = input("> ")
        

    if inp == "c":
        # * adds projectile, mass 10**2 and radius 0.02, indicative
        projectiles.append( e.object(ship.r, ship.theta, to_add[0], to_add[1], 10**2, 0.02)   )
            





