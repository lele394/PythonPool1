import physical_constants as pc
from math import *


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


