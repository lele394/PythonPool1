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



    #get a list of l0
    l0s = [compute_l0(obj.r, obj.vtheta) for obj in objects]

    #creates deltat variable
    deltat = initialDeltat

    #initialise theta list
    # theta_list = [[0, obj.theta] for obj in objects]




    #initialize v_list?
    for obj in objects:
        obj.v_list = [obj.vr + acceleration(blackhole.m, obj.r_list[0], obj.l0)]



    rem_time = datetime.now()
    #for each step
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
        rs = [] 
        thetas = []
        for obj in objects:
            rs.append(obj.r_list[-1])
            thetas.append(obj.theta_list[-1])



        """
        # ~ Collision stuff hereeee
        if i < conf._collisionGracePeriod: col = []
        else: col = DetectCollisions(rs, thetas, objects)
        if col != [] and True: #enable debug or not
            print(f'collisions on iteration {i} for objects {col}')
        
        for pair in col:
            update_colliding_objects(pair, objects, r_list, v_list, theta_list, l0s, deltat )
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
            print(len(obj.theta_list))


            # * updates lists of objects with new one
            # ! innefecient as FUCK, udate to just add the last value cuz holy shit that must slow down this bitch so bad
 



            # ~ escape conditions
            if obj.r_list[-1] < conf._outOfBoundMin or obj.r_list[-1] > conf._outOfBoundMax:

                if obj.r_list[-1] < conf._outOfBoundMin: print(f'object fell in blackhole, remaining objects before pop : {len(objects)}, iteration number {i}')
                if obj.r_list[-1] > conf._outOfBoundMax: print(f'object escape, remaining objects before pop : {len(objects)}, iteration number {i}')

                finished_objects.append(obj)

                # * gets rid of the data in r, v and theta lists, and deletes the l0
                objects_to_depop.append(obj)


        # * dels all specified objects to depop
        for obj_to_remove in objects_to_depop:
            objects.remove(obj_to_remove)

    # * writes all remaining objects to the output list


    return finished_objects + objects





















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











def update_colliding_objects(pair: (int, int), objects: list[object], r_list, v_list, theta_list, l0s, deltat):
    
    a = objects[pair[0]]
    b = objects[pair[1]]

    ia = pair[0]
    ib = pair[0]

    atheta_p = (theta_list[ia][-1] - theta_list[ia][-2]) / deltat
    btheta_p = (theta_list[ib][-1] - theta_list[ib][-2]) / deltat

    ar = r_list[ia][-1]
    br = r_list[ib][-1]

    ar_p = v_list[ia][-1]
    br_p = v_list[ib][-1]


    #1
    v_list[ia].append(((a.m - b.m) * ar_p + 2*b.m* br_p) / (a.m+b.m))
    v_list[ib].append(((b.m - a.m) * br_p + 2*a.m* ar_p) / (a.m+b.m) )

    r_list[ia].append(v_list[ia][-1]*deltat)
    r_list[ib].append(v_list[ib][-1]*deltat)

    ar = r_list[ia][-1]
    br = r_list[ib][-1]

    #2
    atheta_p = ((a.m-b.m)*ar *atheta_p +2*b.m *br *btheta_p)/((a.m+b.m)*ar)
    btheta_p = ((b.m-a.m)*br *btheta_p -2*a.m *ar *atheta_p)/((b.m+a.m)*br)

    theta_list[ia].append(atheta_p*deltat)
    theta_list[ib].append(btheta_p*deltat)


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



    # r_list[pair[0]].append(vr1_final * deltat + r_list[pair[0]][-1])
    # r_list[pair[1]].append(vr2_final * deltat + r_list[pair[1]][-1])
    
    # theta_list[pair[0]].append(vtheta1_final * deltat + theta_list[pair[0]][-1])
    # theta_list[pair[1]].append(vtheta2_final * deltat + theta_list[pair[1]][-1])
    return




