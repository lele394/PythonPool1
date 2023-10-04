from math import *
from .physicalConstants import pi

import numpy as np







def pol_vel_to_car(vr, vtheta, theta):
    vx = vr * np.cos(theta) - vtheta * np.sin(theta)
    vy = vr * np.sin(theta) + vtheta * np.cos(theta)
    return vx, vy

def car_vel_to_pol(vx, vy, theta):
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


        #check for particles of indices n-1
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

                #removes spawn flag
                if p.type == "Ship"and n.type == "Light" and "SpawnedOnShip" in n.WasColliding:
                    n.WasColliding.remove("SpawnedOnShip")
                if n.type == "Ship"and p.type == "Light" and "SpawnedOnShip" in p.WasColliding:
                    p.WasColliding.remove("SpawnedOnShip")




    return collisions









def DotProduct(x1, x2, y1, y2):
    #https://physics.stackexchange.com/questions/258943/dot-product-of-two-vectors-in-spherical-polar-coordinates-do-i-have-to-convert
    return x1*x2 + y1*y2

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



    """
    # * mmmmmmmmmmmmmm the stuff i made using cartesian conversions
    b = objects[pair[0]]
    a = objects[pair[1]]

    a.UpdateVariables(deltat)
    b.UpdateVariables(deltat)


    m1 = a.m
    m2 = b.m

    # https://lucidar.me/fr/mechanics/elastic-collision-equations-simulation-part-5/
    v1 = (a.r * cos(a.theta), a.r * sin(a.theta))
    v2 = (b.r * cos(b.theta), b.r * sin(b.theta))

    u1 = (a.r * cos(a.theta), a.r * sin(a.theta))
    u2 = (b.r * cos(b.theta), b.r * sin(b.theta))


    alpha1 = atan2(v2[1] - v1[1], v2[0] - v1[0])
    beta1 = atan2(u1[1], u1[0])
    gamma1 = beta1 - alpha1
    u12 = (sqrt(v1[0]**2 + v1[1]**2)) * cos(gamma1)
    u11 = (sqrt(v1[0]**2 + v1[1]**2)) * sin(gamma1)


    alpha2 = atan2(v1[1] - v2[1], v1[0] - v2[0])
    beta2 = atan2(u2[1], u2[0])
    gamma2 = beta2 - alpha2
    u21 = (sqrt(v2[0]**2 + v2[1]**2)) * cos(gamma2)
    u22 = (sqrt(v2[0]**2 + v2[1]**2)) * sin(gamma2)

    v12 = ( (m1-m2)*u12 - 2*m2*u21 ) / (m1+m2)
    v21 = ( (m1-m2)*u21 + 2*m1*u12 ) / (m1+m2)


    V1 = ( u11*(-sin(alpha1)) + v12*cos(alpha1),  u11*cos(alpha1) + v12*sin(alpha1)    )

    V2 = ( u22*(-sin(alpha2)) + v21*cos(alpha2),  u22*cos(alpha2) + v21*sin(alpha2)    )


    rv1 = sqrt( V1[0]**2 + V1[0]**2)
    rv2 = sqrt( V2[0]**2 + V2[0]**2)

    thetav1 = atan2(V1[1], V1[0])
    thetav2 = atan2(V2[1], V2[0])

    a.v_list.append(rv1)
    b.v_list.append(rv2)

    a.r_list.append(   a.r_list[-1] + rv1 *deltat  )
    b.r_list.append(   b.r_list[-1] + rv2 *deltat  )

    a.theta_list.append(  a.theta_list[-1] + thetav1 *deltat )
    b.theta_list.append(  b.theta_list[-1] + thetav2 *deltat )

    print("doing it once")

    a.InvulnerabiltyTo.append(b)
    b.InvulnerabiltyTo.append(a)

    a.UpdateVariables(deltat)
    b.UpdateVariables(deltat)

    a.l0 = compute_l0(a.r, a.vtheta)
    b.l0 = compute_l0(b.r, b.vtheta)

    """
    
    """
    # ! LAST ONE TO SOMEWHAT WORK LAST TIME
    a_o = objects[pair[0]]
    b_o = objects[pair[1]]

    # * duplicating objects to avoid conflict during calculations
    a = a_o#.Copy()
    b = b_o#.Copy()

    atheta_p = (a.theta_list[-1] - a.theta_list[-2]) / deltat
    btheta_p = (b.theta_list[-1] - b.theta_list[-2]) / deltat


    # * calculate the final velocities in polar coordinates
    arp = ((a.m-b.m)*a.v_list[-1]+2*b.m*b.v_list[-1])/(a.m+b.m)
    brp = ((b.m-a.m)*b.v_list[-1]-2*a.m*a.v_list[-1])/(a.m+b.m)
    a_o.v_list.append(arp)
    b_o.v_list.append(brp)

    # * calculate the final angles
    a_o.theta_list.append( a.theta_list[-1] - ((a.m-b.m)*a.r_list[-1]*atheta_p+2*b.m*b.r_list[-1]*btheta_p)/((a.m+b.m)*a.r_list[-1]) * deltat)

    # * add position
    a_o.r_list.append(a.r_list[-1] + arp * deltat)
    b_o.r_list.append(b.r_list[-1] + brp * deltat)
    

    # ! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # a.InvulnerabiltyTo.append(b)
    # b.InvulnerabiltyTo.append(a)

    a.UpdateVariables(deltat)
    b.UpdateVariables(deltat)

    a_o.l0 = compute_l0(a.r, a.vtheta)
    b_o.l0 = compute_l0(b.r, b.vtheta)

    # & gestion of grace period between both objects
    # condition on deltat : 
    # deltat > (Ra + Rb) / (Va - Vb)
    
    """




    #https://stackoverflow.com/questions/35211114/2d-elastic-ball-collision-physics




    a = objects[pair[0]]
    b = objects[pair[1]]



    if a in b.WasColliding or b in a.WasColliding: print("no update as they were already colliding");return





    xa = a.r * cos(a.theta)
    xb = b.r * cos(b.theta)

    ya = a.r * sin(a.theta)
    yb = b.r * sin(b.theta)



    # ! here comes vectorial proj
    """
    vxa = a.vr * cos(a.theta) - a.r * a.vtheta * sin(a.theta)
    vxb = b.vr * cos(b.theta) - b.r * b.vtheta * sin(b.theta)

    vya = a.vr * sin(a.theta) + a.r * a.vtheta * cos(a.theta)
    vyb = b.vr * sin(b.theta) + b.r * b.vtheta * cos(b.theta)
    """


    (vxa, vya) = pol_vel_to_car(a.vr, a.vtheta, a.theta)
    (vxb, vyb) = pol_vel_to_car(b.vr, b.vtheta, b.theta)





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

    # ! vectorial proj lolilol
    """
    nvra = nvxa * cos(a.theta) + nvya * sin(a.theta)
    nvrb = nvxb * cos(b.theta) + nvyb * sin(b.theta)

    nvta = (nvya * cos(a.theta) - nvxa * sin(a.theta)) / a.r
    nvtb = (nvyb * cos(b.theta) - nvxb * sin(b.theta)) / b.r
    """

    (nvra, nvta) = car_vel_to_pol(nvxa, nvya, a.theta)
    (nvrb, nvtb) = car_vel_to_pol(nvxb, nvyb, b.theta)



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











    # print( nvra, nvta )
    # print( nvrb, nvtb )


    #updates l0s
    a.Updatel0()
    b.Updatel0()

    #add eachother to the colliding list
    a.WasColliding.append(objects[pair[1]])
    b.WasColliding.append(objects[pair[0]])

    a.UpdateVariables(deltat)
    b.UpdateVariables(deltat)

    # input()




    # return


