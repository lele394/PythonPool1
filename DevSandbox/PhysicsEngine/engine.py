import physical_constants as pc
from math import *


def escape_velocity(r: float, m: float):
    """
    input :
        r : float
            distance r from the black hole
        
        m : float
            masses of the obeject
        
    return :
        float escape velocity


    return escape velocity based on sqrt(2*g*m / r)
    """

    return sqrt( 2 * pc.G * m / r)






def Schwarzschild_radius(m: float):
    """
    input :
        m : float
            mass of the blackhole

    return :
        float
        scharzschild radius of object
    """

    return (2 * pc.G * m) / (pc.c* pc.c)