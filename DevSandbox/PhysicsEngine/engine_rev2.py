# import PhysicsEngine.physicalConstants as pc
import physicalConstants as pc
from math import *
from datetime import datetime



import config as conf


class object:
    def __init__(self, 
                 r: float, 
                 theta: float, 
                 vr:float, 
                 vtheta: float, 
                 m: float, 
                 radius= 0,
                 ):
        
        self.r = r
        self.theta= theta
        self.vr = vr
        self.vtheta= vtheta
        self.m = m
        self.radius = radius

        self.l0 = compute_l0(self.r, vtheta)

        self.r_list = [r]
        self.theta_list = [ theta]
        self.v_list = [vr]

        self.IsOut = False# if true, means the object is out of the simulation

        self.InvulnerabiltyTo = []

    def UpdateVariables(self, last_deltat):
        self.r = self.r_list[-1]
        self.theta = self.theta_list[-1]
        self.vr = self.v_list[-1]
        self.vtheta = self.GetTheta_p(last_deltat)
    
    def speed(self):
        return (self.vr, self.vtheta)
    
    def speed_norm(self, deltat):
        v = sqrt(self.v_list[-1]**2+self.r_list[-1]**2*self.GetTheta_p(deltat)**2)
        return v

    def position(self):
        return (self.r, self.theta)
    
    def GetR(self):
        return self.r_list[-1]

    def GetTheta(self):
        return self.theta_list[-1]
    
    def GetTheta_p(self, deltat):
        return (self.theta_list[-1] - self.theta_list[-2]) / deltat
    

   




def clamp(num, min_value, max_value):
   """clamp num between min and max"""
   return max(min(num, max_value), min_value)

# def ComputeDeltatT(r: list[float], v: list[float], theta: list[float], prevdeltat: float):*
def ComputeDeltatT(objects: list[object], prevdeltat: float):

    """
    input :
        r : list[float]
            list of all current r value for each objects
        v : list[float]
            list of all the current speed on r (rdot)
        theta : list[list[float]]
            list

    return :
        float
        new minimum deltat that can be used in the simulation
    """

    dt_list = []
    # * part about objects being close to the blackhole
    for object in objects:
        dt = 2 * pc.pi * object.r_list[-1] / (conf._computeDeltaDeltatFactor * object.speed_norm(prevdeltat))
        dt_list.append(dt)


    # * part where objects just jump no more than twice their radius, for collision purposes
    for object in objects:
        dt = 2 * object.radius / object.speed_norm(prevdeltat)
        dt_list.append(dt)



    return min(dt_list)
    return prevdeltat




# ! used to compute the first deltat, because i don't save delta_ps
def deltaless_deltat(objects, override=""):
    """
    input: 
        objects : list[object]
            all objects in the simulation
        override : float
            allows to skip deltat computation and return a desired value as override

    return:
        float
        deltat
    """
    if override != "": return override
    dt_list = []
    for object in objects:
        v = sqrt(object.v_list[-1]**2+object.r_list[-1]**2*object.vtheta**2)
        dt = 2 * pc.pi * object.r_list[-1] / (conf._computeDeltaDeltatFactor * v)
        dt_list.append(dt)

    return min(dt_list)
















def compute_l0(r, vtheta):
    """
    input :
        r: float
            r component of the position
        vtheta :
            theta component of the speed
    """
    return r*r*vtheta



def theta_next(theta: float, l0: float, rk: float, deltat: float) -> float:
    """
    input : float
        theta : initial theta
    l0 : float
        calculated from the initial position
    rk : float
        donno
    deltat :
        time delta between both steps


    UPDATE RK TO THE ALGORITHM IN PDF
    """

    return theta + l0/(rk**2)* deltat





def acceleration(m: float, r: float, l0: float):
    """
    input: 
        m : float
            mass of black hole
        r : float
            radius of the object
        l0 : float
            computed angular momentum
    
    return :
        float
        acceleration
    """
    return  - pc.G * m /r**2 + (r-3/2) * l0**2 / r**4





#Leapfrog integration


def rk_next(rk: float, vk: float, deltat: float):
    """
    input :
    self explnatory

    return:
        return rk+1 for leapfrog
    """

    return rk + vk*deltat


def vk_next(vk: float, rk: float, mass: float, l0:float, deltat: float):
    """
    input :
    self explanatory
    
    return:
        return vk+3/2 for leafrog
    """
    return vk + acceleration(mass, rk, l0) * deltat









def nbody_coupled_integrator(objects: list[object], 
                       blackhole: object, 
                       steps: int, 
                       initialDeltat: float
                       ):
    

    finished_objects = []
    objects_to_depop = []


    #creates deltat variable
    deltat = initialDeltat





    #initialize v_list?
    for obj in objects:
        obj.v_list = [obj.vr + acceleration(blackhole.m, obj.r_list[0], obj.l0)]



    rem_time = datetime.now()
    #for each step
    for i in range(steps):

        # ~ just to print simulation steps and infos
        if i %conf._statusPrintModulo == 0:
            print(f' {int(i/steps * 100)} % \t current deltat : {deltat:.5f} \t step time : {(datetime.now() - rem_time)} \t estimated remaining time : {(datetime.now() - rem_time) * (steps-i)}\t active objects {len(objects)}')
        rem_time = datetime.now()




        #resets depopulation indices
        objects_to_depop = []



        if len(objects) == 0:
            break
            
        #get all last computed rs and vs (and thetas)
        rs = [] 
        thetas = []
        for obj in objects:
            rs.append(obj.r_list[-1])
            thetas.append(obj.theta_list[-1])













        # ~ Collision stuff hereeee
        doNotUpdate = []
        if i < conf._collisionGracePeriod: col = [] # for objects instantiated on top of eachother
        else: col = DetectCollisions(rs, thetas, objects, i)
        if col != [] and conf._debugCollisions:
            print(f'collisions on iteration {i} for objects {col}')
        
        for pair in col:
             update_colliding_objects(pair, objects, deltat)




        for pair in col:
            for i in pair:
                if objects[i] not in doNotUpdate:
                    doNotUpdate.append(objects[i])





        #compute a deltat
        if i!=0 : deltat = ComputeDeltatT(objects, deltat)#do not run on first iteration, need to use deltat passed
        #for each object do 1 step
        for obj in objects:

            #! uncomment
            if obj in doNotUpdate: continue

            # * stuff for r 
            obj.r_list.append( rk_next(obj.r_list[-1], obj.v_list[-1], deltat) )
            obj.v_list.append( vk_next(obj.v_list[-1], obj.r_list[-1], blackhole.m, obj.l0, deltat) )

            # * stuff for theta 
            obj.theta_list.append(theta_next(obj.theta_list[-1], obj.l0, obj.r_list[-1], deltat))



            # ~ escape conditions
            if obj.r_list[-1] < conf._outOfBoundMin or obj.r_list[-1] > conf._outOfBoundMax:

                if obj.r_list[-1] < conf._outOfBoundMin: print(f'object fell in blackhole, remaining objects before pop : {len(objects)}, iteration number {i}'); obj.IsOut = True
                if obj.r_list[-1] > conf._outOfBoundMax: print(f'object escape, remaining objects before pop : {len(objects)}, iteration number {i}'); obj.IsOut = True

                finished_objects.append(obj)

                # * gets rid of the data in r, v and theta lists, and deletes the l0
                objects_to_depop.append(obj)


        # * dels all specified objects to depop
        for obj_to_remove in objects_to_depop:
            objects.remove(obj_to_remove)

    # * writes all remaining objects to the output list

    return (finished_objects + objects, deltat)
    #                                   ^ deltat is returned cuz needed to initiate nextstep





















# ! collision stuff

def DetectCollisions(r: list[float], theta: list[float], objects: list[object], i: int): 
    """
    input :
        r : list[float]
            contains positions of the particles for r
        theta : list[float]
            contains the position of the particles for theta
        object : list[object]
            list of all objects
        i : int
            number of the iteration

    return:
        list[(int, int)]
        pairs of int corresponding to both objects in a collision
    """

    

    collisions = [] #will get all the pair of colliding objects 

    master = [ (r[i], theta[i]) for i in range(len(r)) ]


    # todo potential opportunity for parallelisation (glsl lol?)
    # check for each particles
    for point in range(len(master)):
        # ! is that even supposed to work?
        rad1 = objects[point].radius
        r1 = master[point][0]
        theta1 = master[point][1]


        #get all object it's invulnerable to
        invulnerable_to = [ l for l in objects[point].InvulnerabiltyTo  ]

        #check for particles of indices n-1
        for neighbor in range(point+1, len(master)):


            # ! is that even supposed to work?
            rad2 = objects[neighbor].radius
            r2 = master[neighbor][0]
            theta2 = master[neighbor][1]

            a = r1**2 +r2**2 - 2 * r1 * r2 * cos(theta2-theta1)
            d = sqrt( abs(a))

            #get distance between 2 points
            if d < (rad1 + rad2):

                #* check if both objects don't have grace periods
                #! looks like i don't need it cuz i'm so good of a physicist | if objects[neighbor] in invulnerable_to: print( f'on {i} object {point} detected collision with {neighbor} but has grace period' );continue
                collisions.append( (point, neighbor) )
    
    return collisions











def update_colliding_objects(pair: (int, int), objects: list[object],  deltat: float):
    



    """
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
    a = objects[pair[0]]
    b = objects[pair[1]]

    atheta_p = (a.theta_list[-1] - a.theta_list[-2]) / deltat
    btheta_p = (b.theta_list[-1] - b.theta_list[-2]) / deltat


    # * calculate the final velocities in polar coordinates
    arp = ((a.m-b.m)*a.v_list[-1]+2*b.m*b.v_list[-1])/(a.m+b.m)
    brp = ((b.m-a.m)*b.v_list[-1]+2*a.m*a.v_list[-1])/(a.m+b.m)
    a.v_list.append(arp)
    b.v_list.append(brp)

    # * calculate the final angles
    a.theta_list.append( a.theta_list[-1] - ((a.m-b.m)*a.r_list[-1]*atheta_p+2*b.m*b.r_list[-1]*btheta_p)/((a.m+b.m)*a.r_list[-1]) * deltat)
    b.theta_list.append( b.theta_list[-1] - ((b.m-a.m)*b.r_list[-1]*btheta_p-2*a.m*a.r_list[-1]*atheta_p)/((b.m+a.m)*b.r_list[-1]) * deltat)

    # * add position
    a.r_list.append(a.r_list[-1] + arp * deltat)
    b.r_list.append(b.r_list[-1] + brp * deltat)
    

    # ! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # a.InvulnerabiltyTo.append(b)
    # b.InvulnerabiltyTo.append(a)

    a.UpdateVariables(deltat)
    b.UpdateVariables(deltat)

    a.l0 = compute_l0(a.r, a.vtheta)
    b.l0 = compute_l0(b.r, b.vtheta)

    # & gestion of grace period between both objects
    # condition on deltat : 
    # deltat > (Ra + Rb) / (Va - Vb)




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

    return








"""#! seems like we don't need those. keeping it here if it happens to become fucky tho.
def UpdateAddObjectsInvulnerabilities(pair: (int, int), objects: list[object],  deltat: float):
    
    a = objects[pair[0]]
    b = objects[pair[1]]
    
    #val alongside r and theta
    val_r = sqrt(a.v_list[-1]**2 + b.v_list[-1]**2)
    val_theta = sqrt(a.r**2 * a.GetTheta_p(deltat)**2 + b.r**2 * b.GetTheta_p(deltat)**2)


    invulnerability = abs((a.radius + b.radius) / max(val_r, val_theta))
    # for a object : #! problem here
    objects[pair[0]].InvulnerabiltyTo.append( [b, invulnerability] )


    # for b object :
    objects[pair[1]].InvulnerabiltyTo.append( [a, invulnerability] )


def UpdateObjectsInvulnerabilities(object: object, deltat: float):

    for invul in object.InvulnerabiltyTo:
        invul[1] -= deltat
    
    object.InvulnerabiltyTo = [ i for i in object.InvulnerabiltyTo if i[1]>0]

"""