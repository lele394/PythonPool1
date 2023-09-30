# import PhysicsEngine.physicalConstants as pc
import physicalConstants as pc
from math import *
from datetime import datetime
from collision import *



import config as conf


class object:
    def __init__(self, 
                 tpe: str,
                 r: float, 
                 theta: float, 
                 vr:float, 
                 vtheta: float, 
                 m: float, 
                 radius= 0,
                 ):
        """
        creates an object class which represent a physical object in the simulation
        has multiple functions attached to itself, namely :

        UpdateVariables( deltat ) :
            input : deltat : float
            return : /
            desc : updates r, theta, vr and vtheta from the list.
                   do not update l0 as it is a movement constant
                   and should only be updated when a collision occurs

        speed_norm( deltat ) :
            input : deltat : float
            return : float norm of the speed vector
            desc : computes and returns the norm of the speed vector

        GetTheta_p( deltat ) :
            input : deltat : float
            return : float derivative of theta
            desc : computes and returns the derivative of theta using
                   the 2 last theta and a deltat specified by the user
                   (usually used after computing last theta)

        Copy() :
            return : new object with the same properties

        ==============
        Creation parameters :
        --------------
            r : float
                radius at which you wish the object to be from the center
            
            theta : float
                angle at which you wish the object to start from

            vr : float
                radial speed the object will have at the start

            vtheta : float
                angular speed the object will have at the start

            m : float
                mass of the projectile

            radius : float (default 0)
                radius of the object


        ==============
        Additional parameters :
        --------------
            l0 : float
                has to be assigned. movement constat used in integration
                Is initialised in the integrator by the program

            r_list : list[float]
                contains all the r coordinates of the object at each steps
                used by the program. use thoses to plot the position
            
            theta_list : list[float]
                contains all the theta coordinates of the object at each steps
                used by the program. use thoses to plot the position

            v_list : list[float]
                contains all the r_p values of the object at each steps
                used by the program.

            IsOut : bool
                indicates if the object is considered "out" of the simulation
                aka it left the boundaires defined in the config file

            InvulnerabilityTo : list[object]
                not implemented
        
        """
        self.type = tpe
        
        self.r = r
        self.theta= theta
        self.vr = vr
        self.vtheta= vtheta
        self.m = m
        self.radius = radius

        self.l0 = compute_l0(self.r, self.vtheta)

        self.r_list = [r]
        self.theta_list = [ theta ]
        self.v_list = [vr]

        self.IsOut = False# if true, means the object is out of the simulation

        self.WasColliding = []

    def UpdateVariables(self, last_deltat):
        self.r = self.r_list[-1]
        self.theta = self.theta_list[-1]
        self.vr = self.v_list[-1]
        self.vtheta = self.GetTheta_p(last_deltat)

    def Updatel0(self):
        self.l0 = compute_l0(self.r, self.vtheta)
    
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
        if len(self.theta_list) == 1: return self.vtheta
        return (self.theta_list[-1] - self.theta_list[-2]) / deltat
    
    def Copy(self):
        obj = object( self.type,
                      self.r,
                      self.theta,
                      self.vr,
                      self.vtheta,
                      self.m,
                      self.radius)
        
        obj.l0 = self.l0

        obj.r_list = self.r_list
        obj.theta_list = self.theta_list
        obj.v_list = self.v_list
        
        return obj
    
    def Debug(self, deltat):
        print( "\n==============================")
        print(f'debugging object {self}')
        print(f'm {self.m}\t radius {self.radius}\t l0 {self.l0}')
        print(f'r {self.r}\t theta {self.theta}')
        print(f'vr {self.vr}\t vtheta {self.vtheta}')
        print(f'last r {self.r_list[-1]}\t last theta {self.theta_list[-1]}')
        print(f'last vr {self.v_list[-1]}\t last vtheta {self.GetTheta_p(deltat)}')
        print(f'==== end debug for {self} ====\n')


    

   




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
    """
    """


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
    """
    does everything
    """
    print(f'\n\n STARTING SIMULATION \n\n')
    

    # objects that are out of the simulation
    finished_objects = []

    deltat_list = []
    collision_iterations = []

    #creates deltat variable
    deltat = initialDeltat






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
            











        # ~ Collision stuff hereeee
        doNotUpdate = []
        col = []
        if i < conf._collisionGracePeriod: col = [] # for objects instantiated on top of eachother
        else: col = DetectCollisions(objects, i, deltat)
        if col != [] and conf._debugCollisions:
            print(f'collisions on iteration {i} for objects {col}')
        if col != []: collision_iterations.append(i)
        """
        
        
        for pair in col:
             if  not( pair == "on grace"):update_colliding_objects(pair, objects, deltat)

        for pair in col:
            if  not( pair == "on grace"):UpdateAddObjectsInvulnerabilities(pair, objects, deltat)

        for obj in objects:
            UpdateObjectsInvulnerabilities(obj, deltat)
        """


        # * objects tht shall not be updated as they already where in the collision
        for pair in col:
            for i in pair:
                if  pair == "on grace": continue
                if objects[i] not in doNotUpdate:
                    doNotUpdate.append(objects[i])





        #compute a deltat
        if i!=0 : deltat = ComputeDeltatT(objects, deltat); deltat_list.append(deltat)#do not run on first iteration, need to use deltat passed
        #for each object do 1 step
        for obj in objects:

            #debug objects
            # print(obj.r_list[-1] , "\t", obj.v_list[-1],"\t", obj.theta_list[-1], "\t", obj.speed_norm(deltat))


            #! uncomment
            if obj in doNotUpdate: continue

            # * stuff for r 
            obj.r_list.append( rk_next(obj.r_list[-1], obj.v_list[-1], deltat) )
            obj.v_list.append( vk_next(obj.v_list[-1], obj.r_list[-1], blackhole.m, obj.l0, deltat) )

            # * stuff for theta 
            obj.theta_list.append(theta_next(obj.theta_list[-1], obj.l0, obj.r_list[-1], deltat) % (2*pc.pi))



            # print(obj.r_list[-1])
            # ~ escape conditions
            if obj.r_list[-1] < conf._outOfBoundMin or obj.r_list[-1] > conf._outOfBoundMax:


                if obj.r_list[-1] < conf._outOfBoundMin: print(f'object fell in blackhole, remaining objects before pop : {len(objects)}, iteration number {i}'); obj.IsOut = True
                if obj.r_list[-1] > conf._outOfBoundMax: print(f'object escape, remaining objects before pop : {len(objects)}, iteration number {i}'); obj.IsOut = True

                finished_objects.append(obj)

                objects_to_depop.append(obj)


        # * dels all specified objects to depop
        for obj_to_remove in objects_to_depop:
            objects.remove(obj_to_remove)
            print(f'depop {obj_to_remove}')

    # * writes all remaining objects to the output list
    return (finished_objects, objects, deltat, deltat_list, collision_iterations)
    #                                   ^ deltat is returned cuz needed to initiate nextstep





