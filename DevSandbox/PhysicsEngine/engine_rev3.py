from .physicalConstants import *
from math import *
from datetime import datetime
from .collision import *



from .config import *


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
        obj.WasColliding = self.WasColliding
        
        return obj
    
    def Debug(self, deltat):
        print( "\n==============================")
        print(f'debugging object {self}')
        print(f'm {self.m}\t radius {self.radius}\t l0 {self.l0}')
        print(f'r {self.r}\t theta {self.theta}')
        print(f'vr {self.vr}\t vtheta {self.vtheta}')
        print(f'last r {self.r_list[-1]}\t last theta {self.theta_list[-1]}')
        print(f'last vr {self.v_list[-1]}\t last vtheta {self.GetTheta_p(deltat)}')
        print(f'Colliding with {self.WasColliding}')
        print(f'==== end debug for {self} ====\n')


    

   





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
    return  - G * m /r**2 + (r-3/2) * l0**2 / r**4





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
    
    deltat = initialDeltat


    for i in range(steps):

        #check for collisions
        pairs = DetectCollisions(objects, i, deltat)


        #for each collisions update objects values
        for pair in pairs:
            if  pair == "on grace": continue
            update_colliding_objects(pair, objects, deltat)

        #ignores colliding objects and update the others
        doNotUpdate = []
        for pair in pairs:
            for i in pair:
                if  pair == "on grace": continue
                if objects[i] not in doNotUpdate:
                    doNotUpdate.append(objects[i])
        doNotUpdate = []

        for obj in objects:
            
            #computes theta
            obj.theta_list.append(theta_next(obj.theta_list[-1], obj.l0, obj.r_list[-1], deltat) % (2*pi))


            #computes r and v (v is radial speed)
            obj.r_list.append( rk_next(obj.r_list[-1], obj.v_list[-1], deltat) )
            obj.v_list.append( vk_next(obj.v_list[-1], obj.r_list[-1], blackhole.m, obj.l0, deltat) )

            obj.UpdateVariables(deltat)

    # returns the right objects
    # for obj in objects:
    #     obj.UpdateVariables(deltat)

    return objects, deltat













    return