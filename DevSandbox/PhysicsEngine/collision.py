from math import *















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


    # todo potential opportunity for parallelisation (glsl lol?)
    # check for each particles
    for point in range(len(objects)):
        p = objects[point]
        p.UpdateVariables(deltat)

        rad1 = p.radius
        r1 = p.r
        theta1 = p.theta


        #get all object it's invulnerable to
        invulnerable_to = p.WasColliding
        # print(invulnerable_to)

        #check for particles of indices n-1
        for neighbor in range(point+1, len(objects)):

            if objects[neighbor] in invulnerable_to: print(f'Iteration {i} : Collision detectd on {(point, neighbor)} but are on grace period'); collisions.append("on grace"); continue

            n = objects[neighbor]
            n.UpdateVariables(deltat)

            rad2 = objects[neighbor].radius
            r2 = n.r
            theta2 = n.theta

            #get distance between 2 points
            a = r1**2 +r2**2 - 2 * r1 * r2 * cos(theta2-theta1)
            d = sqrt( a )

            if d < (rad1 + rad2):

                #* check if both objects don't have grace periods
                #    ^ not here yet
                collisions.append( (point, neighbor) )
    
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


    """
    # ! made in Trigui
    # Calculate the final velocities in polar coordinates
    a.r_p.append(((a.mass-b.mass)*a.r_p[-1]+2*b.mass*b.r_p[-1])/(a.mass+b.mass))
    b.r_p.append(((b.mass-a.mass)*b.r_p[-1]+2*a.mass*a.r_p[-1])/(a.mass+b.mass))
    """
    """
    # Calculate the final angles
    a.theta_p.append(((a.mass-b.mass)*a.r[-1]*a.theta_p[-1]+2*b.mass*b.r[-1]*b.theta_p[-1])/((a.mass+b.mass)*a.r[-1]))
    b.theta_p.append(((b.mass-a.mass)*b.r[-1]*b.theta_p[-1]-2*a.mass*a.r[-1]*a.theta_p[-1])/((b.mass+a.mass)*b.r[-1]))
    """


    #https://stackoverflow.com/questions/35211114/2d-elastic-ball-collision-physics

    a = objects[pair[0]]
    b = objects[pair[1]]

    a.UpdateVariables(deltat)
    b.UpdateVariables(deltat)

    xa = a.r * cos(a.theta)
    xb = b.r * cos(b.theta)

    ya = a.r * sin(a.theta)
    yb = b.r * sin(b.theta)

    vxa = a.vr * cos(a.vtheta)
    vxb = b.vr * cos(b.vtheta)

    vya = a.vr * sin(a.vtheta)
    vyb = b.vr * sin(b.vtheta)



    #for a :
    dpa = DotProduct( vxa-vxb , vya-vyb,  xa-xb , ya-yb  )
    #on r
    axmba = xa-xb
    nvxa = vxa - (2*b.m)/(a.m + b.m) * (dpa / abs(axmba)**2 ) * axmba
    #on theta
    aymby = ya-yb
    nvya = vxa - (2*b.m)/(a.m + b.m) * (dpa / abs(aymby)**2) * aymby


    #for b :
    dpb = DotProduct( vxb-vxa , vyb-vya,  xb-xa , yb-ya  )
    #on r
    xbmxa = xb-xa
    nvxb = vxb - (2*a.m)/(a.m + b.m) * (dpb / abs(xbmxa)**2 ) * xbmxa
    #on theta
    bymay = yb-ya
    nvyb = vyb - (2*a.m)/(a.m + b.m) * (dpb / abs(bymay)**2) * bymay


    nvra = sqrt(nvxa**2 + nvya**2)
    nvta = atan(ya / xa)

    nvrb = sqrt(nvxb**2 + nvyb**2)
    nvtb = atan(yb / xb)

    objects[pair[0]].vr = nvra
    objects[pair[0]].vtheta = nvta

    objects[pair[1]].vr = nvrb
    objects[pair[1]].vtheta = nvtb

    objects[pair[0]].r_list.append(nvra * deltat)
    objects[pair[1]].r_list.append(nvrb * deltat)

    objects[pair[0]].theta_list.append(nvra * deltat)
    objects[pair[1]].theta_list.append(nvrb * deltat)

    #updates l0s
    objects[pair[0]].Updatel0()
    objects[pair[1]].Updatel0()

    #add eachother to the colliding list
    objects[pair[0]].WasColliding.append(objects[pair[1]])
    objects[pair[1]].WasColliding.append(objects[pair[0]])




    return



def UpdateAddObjectsInvulnerabilities(pair: (int, int), objects: list[object],  deltat: float):
    

    a = objects[pair[0]]
    b = objects[pair[1]]
    
    #val alongside r and theta
    val_r = sqrt(a.v_list[-1]**2 + b.v_list[-1]**2)
    val_theta = sqrt(a.r**2 * a.GetTheta_p(deltat)**2 + b.r**2 * b.GetTheta_p(deltat)**2)


    invulnerability = abs((a.radius + b.radius) / max(val_r, val_theta))

    # ! override top calculation, bd idea b oh well
    invulnerability = 0

    # for a object : #! problem here
    objects[pair[0]].InvulnerabiltyTo.append( [b, invulnerability] )

    # for b object :
    objects[pair[1]].InvulnerabiltyTo.append( [a, invulnerability] )


def UpdateObjectsInvulnerabilities(object: object, deltat: float):

    for invul in object.InvulnerabiltyTo:
        # invul[1] -= deltat
        invul[1] -= 1 # ! because of override in prev function
    
    object.InvulnerabiltyTo = [ i for i in object.InvulnerabiltyTo if i[1]>0]
