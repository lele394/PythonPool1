from math import cos, sin, sqrt

import numpy as np







def pol_vel_to_car(vr, vtheta, theta):
    """
    input :
        vr : float
            speed on r

        vtheta : float
            speed on theta

        theta : float
            angle 
    
    return :
        vx, vy: floats
            coordinates of the vector in cartesian coordinates
    """
    vx = vr * np.cos(theta) - vtheta * np.sin(theta)
    vy = vr * np.sin(theta) + vtheta * np.cos(theta)
    return vx, vy

def car_vel_to_pol(vx, vy, theta):
    """
    input :
        vx : float
            speed on x

        vy : float
            speed on y

        theta : float
            angle 
    
    return :
        vr, vtheta: floats
            coordinates of the vector in polar coordinates
    """
    vr = vx * np.cos(theta) + vy * np.sin(theta)
    vtheta = vy * np.cos(theta) - vx * np.sin(theta)
    return vr, vtheta












# ! collision stuff

def DetectCollisions(objects: list[object], i: int, deltat: float): 
    """
    input :
        object : list[object]
            list of all objects
        i : int
            number of the iteration

    return:
        list[(int, int)]
        pairs of int corresponding to both objects in a collision
    """

    

    collisions = [] #will get all the pair of colliding objects 

    # master = [ (r[i], theta[i]) for i in range(len(r)) ]


    # check for each particles
    for point in range(len(objects)):
        p = objects[point]
        p.UpdateVariables(deltat)

        rad1 = p.radius
        r1 = p.r
        theta1 = p.theta


        #check for particles of indices n-1, previous pairs being already checked
        for neighbor in range(point+1, len(objects)):

            n = objects[neighbor]
            n.UpdateVariables(deltat)

            rad2 = objects[neighbor].radius
            r2 = n.r
            theta2 = n.theta

            #get distance between 2 points
            a = r1**2 +r2**2 - 2 * r1 * r2 * cos(theta2-theta1)
            d = sqrt( a )

            #if colliding
            if d < (rad1 + rad2):

                if objects[neighbor] in p.WasColliding: print(f'Iteration {i} : Collision detectd on {(point, neighbor)} but were colliding before'); collisions.append("on grace"); continue
                collisions.append( (point, neighbor) )

            #if not colliding remove the spawn tag and eachother from lists
            else :
                if n in p.WasColliding:
                    p.WasColliding.remove(n)
                if p in n.WasColliding:
                    n.WasColliding.remove(p)

                #removes spawn tag. gme dependent here sooooo update as you please
                if p.type == "Ship"and n.type == "Light" and "SpawnedOnShip" in n.WasColliding:
                    n.WasColliding.remove("SpawnedOnShip")
                if n.type == "Ship"and p.type == "Light" and "SpawnedOnShip" in p.WasColliding:
                    p.WasColliding.remove("SpawnedOnShip")




    return collisions











def update_colliding_objects(pair: (int, int), objects: list[object],  deltat: float):
    """
    input :
        pair : (int, int)
            pair of object where a collision is detected

        objects : list[object]
            list of all object present in the simulation

        deltat : float
            deltat that should be used for the step


    updates objects with a collision
    """


    #https://stackoverflow.com/questions/35211114/2d-elastic-ball-collision-physics



    # for readablity 
    a = objects[pair[0]]
    b = objects[pair[1]]


    # check for collisions previous to that step
    # ensures we don't collide 2 objects twice as
    # they might still be in eachother after a time step depending on their speec
    if a in b.WasColliding or b in a.WasColliding: print("no update as they were already colliding");return




    # converts polar coordinates to cartesian
    xa = a.r * cos(a.theta)
    xb = b.r * cos(b.theta)

    ya = a.r * sin(a.theta)
    yb = b.r * sin(b.theta)


    # polar to cartesian for the speed vectors
    # ! here comes vectorial proj
    (vxa, vya) = pol_vel_to_car(a.vr, a.vtheta, a.theta)
    (vxb, vyb) = pol_vel_to_car(b.vr, b.vtheta, b.theta)




    # * computing new speed vector componnents for objects a and b 
    #for a :
    dpa = np.dot( (vxa-vxb , vya-vyb),  (xa-xb , ya-yb)  )
    #on r
    namb = sqrt( (xa-xb)**2 + (ya-yb)**2 )
    nvxa = vxa - (2*b.m)/(a.m + b.m) * (dpa / namb**2 ) * (xa-xb)
    #on theta
    nvya = vya - (2*b.m)/(a.m + b.m) * (dpa / namb**2) * (ya-yb)


    #for b :
    dpb = np.dot( (vxb-vxa , vyb-vya),  (xb-xa , yb-ya)  )
    #on r
    nbma = sqrt( (xb-xa)**2 + (yb-ya)**2 )
    nvxb = vxb - (2*a.m)/(a.m + b.m) * (dpb / nbma**2 ) * (xb-xa)
    #on theta
    nvyb = vyb - (2*a.m)/(a.m + b.m) * (dpb / nbma**2) * (yb-ya)


    # back to polar for the speed
    # ! vectorial proj lolilol
    (nvra, nvta) = car_vel_to_pol(nvxa, nvya, a.theta)
    (nvrb, nvtb) = car_vel_to_pol(nvxb, nvyb, b.theta)


    # attributing new variables to both objects
    a.vr = nvra
    a.vtheta = nvta

    b.vr = nvrb
    b.vtheta = nvtb

    a.r_list.append(a.r_list[-1] +  nvra * deltat)
    b.r_list.append(b.r_list[-1] +  nvrb * deltat)

    a.theta_list.append(    a.theta_list[-1] + nvta * deltat    )
    b.theta_list.append(    b.theta_list[-1] + nvtb * deltat    )


    a.v_list.append((a.r_list[-1] - a.r_list[-2])/deltat)
    b.v_list.append((b.r_list[-1] - b.r_list[-2])/deltat)



    #updates l0s
    a.Updatel0()
    b.Updatel0()

    #add eachother to the colliding list
    a.WasColliding.append(objects[pair[1]])
    b.WasColliding.append(objects[pair[0]])

    # variables updates to make sure, might already be implemented
    # at the end of the game loop, might wanna check and get rid of this one
    a.UpdateVariables(deltat)
    b.UpdateVariables(deltat)



