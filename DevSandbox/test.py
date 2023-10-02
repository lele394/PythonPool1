import PhysicsEngine.engine_rev2 as e
import PhysicsEngine.physicalConstants as pc
import matplotlib.pyplot as plt
from math import sqrt, radians, cos, sin

outOfBound =  40
inOfBound = 0

steps = 100000

deltat = 0.01



bh = e.object("Blackhole", 0,0,0,0,10**12)




def GetCircularVelocity(r: float):
    return sqrt(pc.G * bh.m / r**2  )


vel = 0.03


deltatt_list = []
collisions_list = []


projs = [
   # e.object(7, 0, 0, -0.043, 10**4, 0.05),
    e.object("Heavy", 35, pc.pi, 0, vel, 1, 1), #red
    e.object("Ship", 35, 0, 0, -vel,  1, 0.1), #blue
]



deltat = e.deltaless_deltat(projs)
print(f'initial deltat {deltat}')


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
projectiles = list(projs)

inp = ""

#sets darck background
# plt.style.use('dark_background')

while inp != "q":

    projs = list(projs)


    # for p in projs:
        # p.Debug(deltat)
    # print(projs)
    (outs, projs, deltat, dt_list, col_list) = e.nbody_coupled_integrator(projs, bh, steps, deltat)
    deltatt_list = deltatt_list+dt_list
    collisions_list = collisions_list + col_list
    projectiles = projs + outs
    # print(projectiles)

    # for p in projectiles:
    #     p.Debug(deltat)



    print(deltat)
    plt.close()

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    #sets boundaries
    ax.set_ylim([inOfBound,outOfBound])
    # ! uncomment next to show blackhole, conflicts when debugging, god knows why
    circle = plt.Circle((0, 0), 1, transform=ax.transData._b, color="red", alpha=0.4)
    ax.add_artist(circle)

    
    # * used as a temporary holder for below's POC
    tempo_coordinates = []
    
    for proj in projectiles:
        theta = proj.theta_list
        r = proj.r_list
        tempo_coordinates.append([list(theta), list(r)])

        match proj.type:
            case "Ship":
                col = "blue"
            case "Heavy":
                col = "red"
            case "Explosive":
                col = "cyan"
            case _:
                col = "yellow"
        
        cx = proj.r_list[-1] * cos(proj.theta_list[-1])
        cy = proj.r_list[-1] * sin(proj.theta_list[-1])
        circle = plt.Circle((cx ,cy ), proj.radius, transform=ax.transData._b, color=col, alpha=0.2)
        ax.add_artist(circle)

        # ax.plot(theta, r, color=col)
        # ax.plot(theta, r, linestyle="", marker=".", color=col)
        # print(len(r), len(theta))
        ax.scatter(theta[-steps:], r[-steps:], marker=".", color=col, s=0.1)

    #reset objects
    """
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
    """

    if projs == []:
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

    if "ppos" in inp:
        for obj in projectiles:
            print(obj.r, obj.theta)

    if "plotdt" in inp:
        print(f'current deltat {deltat}\t {len(deltatt_list)} deltats saved')

        fig2, ax2 = plt.subplots()
        ax2.plot([i for i in range(len(deltatt_list))], deltatt_list)
        fig2.show()
        input("dt/step plotted, enter to continue > ")

    if "plotall" in inp:
        fig2, ax2 = plt.subplots(subplot_kw={'projection': 'polar'})
        for proj in projectiles:
            theta = proj.theta_list
            r = proj.r_list
            match proj.type:
                case "Ship":
                    col = "blue"
                case "Heavy":
                    col = "red"
                case _:
                    col = "yellow"
            ax2.scatter(theta, r, marker=".", color=col, s=0.001)
        circle = plt.Circle((0, 0), 1, transform=ax.transData._b, color="red", alpha=0.4)
        ax.add_artist(circle)
        fig2.show()
        input("all steps plotted, enter to continue > ")

    if "plotobjectsdeltas" in inp:
        deltastheta = [ ((projectiles[1].theta_list[i] - projectiles[0].theta_list[i]) % (15 * pc.pi))/40   for i in range(len(projectiles[1].theta_list))  ]
        deltasr = [ projectiles[0].r_list[i] - projectiles[1].r_list[i]   for i in range(len(projectiles[0].r_list))  ]
        fig2, ax2 = plt.subplots()
        ax2.plot([i for i in range(len(deltastheta))], deltastheta, label="theta" )
        ax2.plot([i for i in range(len(deltasr))], deltasr, label="r" )
        ax2.scatter(collisions_list, [0 for i in range(len(collisions_list))], label="collisions detected", marker=".", color="red", s= 0.5)
        fig2.legend()
        fig2.show()
        input("all deltas plotted, enter to continue > ")



        



    
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
            





