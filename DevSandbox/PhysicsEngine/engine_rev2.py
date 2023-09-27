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
                 radius= 0):
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

    def UpdateVariables(self, last_deltat):
        self.r = self.r_list[-1]
        self.theta = self.theta_list[-1]
        self.vr = self.v_list[-1]
        self.vtheta = self.GetTheta_p(last_deltat)
    
    def speed(self):
        return (self.vr, self.vtheta)

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
    v=0
    dt_list = []
    for object in objects:


        v = sqrt(
            ((object.r_list[-1] - object.r_list[-1])/prevdeltat) ** 2 
            + 
            object.r_list[-1]**2 * ((object.theta_list[-1] - object.theta_list[-2])/prevdeltat)**2)


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
            print(f' {int(i/steps * 100)} % \t current deltat : {deltat:.5f} \t step time : {(datetime.now() - rem_time)} \t estimated remaining time : {(datetime.now() - rem_time) * (steps-i)}')
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
        if i < conf._collisionGracePeriod: col = []
        else: col = DetectCollisions(rs, thetas, objects)
        if col != [] and True: #enable debug or not
            print(f'collisions on iteration {i} for objects {col}')
        
        for pair in col:
            update_colliding_objects(pair, objects, deltat)
        """
        """

       


        #compute a deltat
        if i!=0 : deltat = ComputeDeltatT(objects, deltat)#do not run on first iteration, need to use deltat passed
        #for each object do 1 step
        for obj in objects:

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

def DetectCollisions(r: list[float], theta: list[float], objects: list[object]): 
    """
    input :
        r : list[float]
            contains positions of the particles for r
        theta : list[float]
            contains the position of the particles for theta

    return:
        list[(int, int)]
        pairs of int corresponding to both objects in a collision
    """

    

    collisions = [] #will get all the pair of colliding objects 

    master = [ (r[i], theta[i]) for i in range(len(r)) ]

    # check for each particles
    for point in range(len(master)):
        # ! is that even supposed to work?
        rad1 = objects[point].radius
        r1 = master[point][0]
        theta1 = master[point][1]
        #check for particles of indices n-1
        for neighbor in range(point+1, len(master)):
            # ! is that even supposed to work?
            rad2 = objects[neighbor].radius
            r2 = master[neighbor][0]
            theta2 = master[neighbor][1]

            # print(f'rad1 {rad1}, rad2 {rad2}')
            a = r1**2 +r2**2 - 2 * r1 * r2 * cos(theta2-theta1)
            d = sqrt( abs(a))
            #print(d)

            #get distance between 2 points

            if d < (rad1 + rad2):
                collisions.append( (point, neighbor) )
    
    return collisions











def update_colliding_objects(pair: (int, int), objects: list[object],  deltat: float):
    
    a = objects[pair[0]]
    b = objects[pair[1]]

    atheta_p = (a.theta_list[-1] - a.theta_list[-2]) / deltat
    btheta_p = (b.theta_list[-1] - b.theta_list[-2]) / deltat

    # * calculate the final velocities in polar coordinates
    a.v_list.append(((a.m-b.m)*a.v_list[-1]+2*b.m*b.v_list[-1])/(a.m+b.m))
    b.v_list.append(((b.m-a.m)*b.v_list[-1]+2*a.m*a.v_list[-1])/(a.m+b.m))

    # * calculate the final angles
    a.theta_list.append(((a.m-b.m)*a.r_list[-1]*atheta_p+2*b.m*b.r_list[-1]*btheta_p)/((a.m+b.m)*a.r_list[-1]) * deltat)
    b.theta_list.append(((b.m-a.m)*b.r_list[-1]*btheta_p-2*a.m*a.r_list[-1]*atheta_p)/((b.m+a.m)*b.r_list[-1]) * deltat)

    # * add position
    a.r_list.append(a.v_list[-1] * deltat)
    b.r_list.append(b.v_list[-1] * deltat)

    # print('=========================')
    # print(a.theta_list[-1])
    # print(b.theta_list[-1])
    # print(a.r_list[-1])
    # print(b.r_list[-1])

    """
    ia = pair[0]
    ib = pair[0]

    atheta_p = (a.theta_list[-1] - a.theta_list[-2]) / deltat
    btheta_p = (b.theta_list[-1] - b.theta_list[-2]) / deltat

    ar = a.r_list[-1]
    br = b.r_list[-1]

    ar_p = a.v_list[-1]
    br_p = b.v_list[-1]


    #1
    a.v_list.append(((a.m - b.m) * ar_p + 2*b.m* br_p) / (a.m+b.m))
    b.v_list.append(((b.m - a.m) * br_p + 2*a.m* ar_p) / (a.m+b.m) )

    a.r_list.append(a.v_list[-1]*deltat)
    b.r_list.append(b.v_list[-1]*deltat)

    ar = a.r_list[-1]
    br = b.r_list[-1]

    #2
    atheta_p = ((a.m-b.m)*ar *atheta_p +2*b.m *br *btheta_p)/((a.m+b.m)*ar)
    btheta_p = ((b.m-a.m)*br *btheta_p -2*a.m *ar *atheta_p)/((b.m+a.m)*br)

    a.theta_list.append(atheta_p*deltat)
    b.theta_list.append(btheta_p*deltat)

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

    return




