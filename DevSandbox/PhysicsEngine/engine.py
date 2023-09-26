# import PhysicsEngine.physicalConstants as pc
import physicalConstants as pc
from math import *

import config as conf


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
   




def clamp(num, min_value, max_value):
   """clamp num between min and max"""
   return max(min(num, max_value), min_value)

def ComputeDeltatT(r: list[float], v: list[float], theta: list[float]):
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
    # print(r,v)
    mini = r[0]
    count = 0
    minivr = v[0]
    theta = theta[0]
    """
    """
    for radius in r: 
        if radius<mini: 
            mini=radius
            miniv = v[count]
        count += 1
    # print(f'mini {mini}\nminiv {minivr}')



    # sqrt(r.**2 + r*theta.**2)
    v = sqrt( minivr ** 2 + (theta[-1] - (minivr ** 2) * theta[-2]) ** 2 )


    deltat = (-1) * 2 * pc.pi * mini / (conf._computeDeltaDeltatFactor *v)
    # print(f'deltat : {deltat}')
    return clamp(abs(deltat), conf._computeDeltaClamp[0], conf._computeDeltaClamp[1])














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











def coupled_integrator(object: object, 
                       blackhole: object, 
                       steps: int, 
                       l0: float, 
                       deltat: float):

    theta = [object.theta]


    #leapfrog
    r = [object.r]
    v = [object.vr + acceleration(blackhole.m, r[0], l0)]

    for i in range(steps):

        #leapfrog
        r.append( rk_next(r[-1], v[-1], deltat) )
        v.append( vk_next(v[-1], r[-1], blackhole.m, l0, deltat) )


        #theta
        theta.append(theta_next(theta[-1], l0, r[-1], deltat))

        # ! NEEDS TO BE CHANGED WHEN USING MULTIPLE OBJECTS
        deltat = ComputeDeltatT([r[-1]], [v[-1]], [theta])

        #stop if under Rs
        if r[-1] < 1 or r[-1] > 16:
            # r.pop()
            # theta.pop()
            return(r, theta)

    return (r, theta)















def nbody_coupled_integrator(object: object, 
                       blackhole: object, 
                       steps: int, 
                       l0: float, 
                       deltat: float):

    theta = [object.theta]


    #leapfrog
    r = [object.r]
    v = [object.vr + acceleration(blackhole.m, r[0], l0)]

    for i in range(steps):

        #leapfrog
        r.append( rk_next(r[-1], v[-1], deltat) )
        v.append( vk_next(v[-1], r[-1], blackhole.m, l0, deltat) )


        #theta
        theta.append(theta_next(theta[-1], l0, r[-1], deltat))

        # ! NEEDS TO BE CHANGED WHEN USING MULTIPLE OBJECTS
        deltat = ComputeDeltatT([r[-1]], [v[-1]], [theta])

        #stop if under Rs
        if r[-1] < 1 or r[-1] > 16:
            # r.pop()
            # theta.pop()
            return(r, theta)

    return (r, theta)