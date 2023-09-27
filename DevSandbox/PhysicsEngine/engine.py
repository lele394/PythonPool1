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

        self.r_list = [r]
        self.theta_list = [theta]
    
    def speed(self):
        return (self.vr, self.vtheta)

    def position(self):
        return (self.r, self.theta)
   




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


    print(prevdeltat)
    # sqrt(r.**2 + r**2 * theta.**2)
    v = sqrt( minivr ** 2 + (minivr ** 2) * (theta[-1] - theta[-2]  / prevdeltat) ** 2 )


    deltat =  2 * pc.pi * mini / (conf._computeDeltaDeltatFactor *v)
    # print(f'deltat : {deltat}')
    return clamp(abs(deltat), conf._computeDeltaClamp[0], conf._computeDeltaClamp[1])

    """












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
        deltat = ComputeDeltatT([r[-1]], [v[-1]], [theta], deltat)

        #stop if under Rs
        if r_list[obj_index][-1] < conf._outOfBoundMin or r_list[obj_index][-1] > conf._outOfBoundMax:
            # r.pop()
            # theta.pop()
            return(r, theta)

    return (r, theta)















def nbody_coupled_integrator(objects: list[object], 
                       blackhole: object, 
                       steps: int, 
                       initialDeltat: float
                       ):
    

    finished_objects = []



    #get a list of l0
    l0s = [compute_l0(obj.r, obj.vtheta) for obj in objects]

    #creates deltat variable
    deltat = initialDeltat

    #initialise theta list
    theta_list = [[0, obj.theta] for obj in objects]
    r_list = [[obj.r] for obj in objects]

    v_list = [[objects[i].vr + acceleration(blackhole.m, r_list[i][0], l0s[i])]  
              for i in range(len(objects))]


    objects_to_depop = []
    #for each step

    rem_time = datetime.now()
    for i in range(steps):

        # ~ just to print simulation steps and infos
        if i %300 == 0:
            print(f' {int(i/steps * 100)} % \t current deltat : {deltat:.5f} \t step time : {(datetime.now() - rem_time)} \t estimated remaining time : {(datetime.now() - rem_time) * (steps-i)}')
        rem_time = datetime.now()




        #resets depopulation indices
        objects_to_depop = []



        if len(objects) == 0:
            break
            
        #get all last computed rs and vs (and thetas)
        rs = [ item[-1] for item in r_list] 
        vs = [ item[-1] for item in v_list]
        thetas = [ item[-1] for item in theta_list]

        # ~ Collision stuff hereeee
        if i < conf._collisionGracePeriod: col = []
        else: col = DetectCollisions(rs, thetas, objects)
        if col != [] and True: #enable debug or not
            print(f'collisions on iteration {i} for objects {col}')
        
        for pair in col:
            object_pair = ( 
                objects[pair[0]],
                objects[pair[1]]
             )
            update_colliding_objects(object_pair, r_list, v_list, theta_list, l0s, deltat )
            

       


        #compute a deltat
        if i!=0 : deltat = ComputeDeltatT(objects, deltat)#do not run on first iteration, need to use deltat passed
        #for each object do 1 step
        for obj_index in range(len(objects)):

            # * stuff for r | uses r_list, v_list, deltat, l0s
            r_list[obj_index].append( rk_next(r_list[obj_index][-1], v_list[obj_index][-1], deltat) )
            v_list[obj_index].append( vk_next(v_list[obj_index][-1], r_list[obj_index][-1], blackhole.m, l0s[obj_index], deltat) )

            # * stuff for theta | uses theta_list, l0s, r_list
            theta_list[obj_index].append(theta_next(theta_list[obj_index][-1], l0s[obj_index], r_list[obj_index][-1], deltat))


            # * updates lists of objects with new one
            objects[obj_index].r_list = list(r_list[obj_index])
            objects[obj_index].theta_list = list(theta_list[obj_index][1:])



            # ~ escape conditions
            if r_list[obj_index][-1] < conf._outOfBoundMin or r_list[obj_index][-1] > conf._outOfBoundMax:

                if r_list[obj_index][-1] < conf._outOfBoundMin: print(f'object fell in blackhole, remaining objects before pop : {len(objects)}, iteration number {i}')
                if r_list[obj_index][-1] > conf._outOfBoundMax: print(f'object escape, remaining objects before pop : {len(objects)}, iteration number {i}')

                finished_objects.append(objects[obj_index])

                # * gets rid of the data in r, v and theta lists, and deletes the l0
                objects_to_depop.append(obj_index)


        # * dels all specified objects to depop
        objects_to_depop.reverse()
        for obj_index in objects_to_depop:
            theta_list.pop(obj_index)
            r_list.pop(obj_index)
            v_list.pop(obj_index)
            l0s.pop(obj_index)
            objects.pop(obj_index)

    # * writes all remaining objects to the output list
    while objects != []:

        finished_objects.append(objects[-1])


        # * gets rid of the data in r, v and theta lists, and deletes the l0
        theta_list.pop(-1)
        r_list.pop(-1)
        v_list.pop(-1)
        l0s.pop(-1)
        objects.pop(-1)

    return finished_objects





















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










# def elastic_collision_(r1, theta1, vr1, vtheta1, m1, r2, theta2, vr2, vtheta2, m2):
def elastic_collision(obj1: object, obj2: object, deltat: float):


    # * gets data fo object 1
    m1 = obj1.m
    r1 = obj1.r_list[-1]
    vr1 = (r1-obj1.r_list[-2])/deltat
    theta1 =obj1.theta_list[-1]
    vtheta1 = (theta1-obj1.theta_list[-2])/deltat

    # * gets data fo object 2
    m2 = obj2.m
    r2 = obj2.r_list[-1]
    vr2 = (r1-obj2.r_list[-2])/deltat
    theta2 =obj2.theta_list[-1]
    vtheta2 = (theta1-obj2.theta_list[-2])/deltat





    # * Convert angles from degrees to radians
    theta1 = radians(theta1)
    theta2 = radians(theta2)
    
    # * Calculate initial momenta in both radial and angular directions
    pr1_initial = m1 * vr1
    pr2_initial = m2 * vr2
    ptheta1_initial = m1 * r1 * vtheta1
    ptheta2_initial = m2 * r2 * vtheta2
    
    # * Calculate the relative velocities in both radial and angular directions
    delta_r = r1 - r2
    delta_theta = theta1 - theta2
    
    relative_vr = vr1 - vr2
    relative_vtheta = r1 * vtheta1 - r2 * vtheta2
    
    # * Calculate the relative momenta in both radial and angular directions
    relative_pr = pr1_initial - pr2_initial
    relative_ptheta = ptheta1_initial - ptheta2_initial
    
    # * Calculate the final velocities using the elastic collision equations
    vr1_final = (2 * m2 * vr2 + pr1_initial - pr2_initial) / (m1 + m2)
    vr2_final = (2 * m1 * vr1 + pr2_initial - pr1_initial) / (m1 + m2)
    
    vtheta1_final = (relative_vtheta + relative_pr * delta_r) / (m1 + m2)
    vtheta2_final = (relative_vtheta + relative_pr * delta_r) / (m1 + m2)
   



def update_colliding_objects(pair: (object, object), r_list, v_list, theta_list, l0s, deltat):
    
    elastic_collision(pair[0], pair[1], deltat)

    
    return