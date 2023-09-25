import physical_constants as pc
from math import *



class object:
    def __init__(self, r, theta, vr, vtheta, m):
        self.r = r
        self.theta= theta
        self.vr = vr
        self.vtheta= vtheta
        self.m = m
    
    def speed(self):
        return (self.vr, self.vtheta)

    def position(self):
        return (self.r, self.theta)
   



















def escape_velocity(r: float, m_bh: float) -> float:
    """
    input :
        r : float
            distance r from the black hole
        
        m_bh : float
            masses of the black hole
    return :
        float escape velocity


    return escape velocity based on sqrt(2*g*m_bh / r)
    """

    return sqrt( 2 * pc.G * m_bh / r)






def Schwarzschild_radius(m_bh: float) -> float:
    """
    input :
        m_bh : float
            mass of the blackhole

    return :
        float
        scharzschild radius of object
    """

    return (2 * pc.G * m_bh) / (pc.c* pc.c)





def gravitational_force(r: float, m_bh: float, m: float) -> float:
    """
    input:
        r : float
            distance between the two objects
        m_bh : float
            mass of the black hole
        m : float
            mass of the orbiting object 

        return :
            gravitational attraction between both objects
    """

    return (- ( pc.G * m_bh) / r**2) * m





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


def Leapfrog_integrator(object: object, blackhole: object, steps: int, l0: float, deltat: float):

    r = [object.r]
    v = [object.vr + acceleration(blackhole.m, r[0], l0)]

    for i in range(steps):
        r.append( rk_next(r[-1], v[-1], deltat) )
        v.append( vk_next(v[-1], r[-1], blackhole.m, l0, deltat) )

    return (r, v)













