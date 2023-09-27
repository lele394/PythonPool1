import scipy as sp
import numpy as np

def acceleration(r_k,l0, hole):
    return -sp.constants.G*hole.mass/r_k**2+(r_k-3/2)*l0**2/r_k**4


def angle_valuation(angle_k,r_k,l0,dt):
    return angle_k+(l0/r_k**2)*dt

def distance_valuation(r_k, r_p_k_1_2, l0, dt, hole):
    r_k_1 = r_k+r_p_k_1_2*dt
    v_k_3_2 = r_p_k_1_2+acceleration(r_k, l0,hole)*dt
    return r_k_1, v_k_3_2
    
def v_echap(object, hole):
    return np.sqrt(2*sp.constants.G*hole.mass/object.r[-1])

def distance(a,b):
    return np.sqrt(a.r[-1]**2+b.r[-1]**2-2*a.r[-1]*b.r[-1]*np.cos(a.theta[-1]-b.theta[-1]))
    
def check_collision(object):
    for i in object.instances:
        for j in object.instances:
            if i!=j and i.etat==1 and j.etat==1:
                if distance(i,j)<(i.radius+j.radius):
                    i.etat=0
                    j.etat=0
    return

def run(object, hole, max_dt, ntime_step):
    stop = 0
    dt_array = []
    dt = [max_dt]
    for obj in object.instances:
        dt.append(2*np.pi*obj.r[-1]/(100*obj.speed())) #Find a condition in term of the orbit
    dt_array.append(min(dt))
    dt = dt_array[-1]
    n = round(ntime_step/dt)

    for i in range(n):
        for obj in object.instances:
            if obj.etat == 1:
                if i == 0:
                    obj.r_p_k_1_2 = obj.r_p[0]+acceleration(obj.r[0], obj.l0, hole)*dt
                
                #if i<5:
                    #print(obj.r)
                # Boucle temporaire pour les tests
                obj.theta.append(angle_valuation(obj.theta[i], obj.r[i], obj.l0,dt))
                obj.theta_p.append((obj.theta[-1]-obj.theta[-2])/dt)
                r_temp, obj.r_p_k_1_2 = distance_valuation(obj.r[i], obj.r_p_k_1_2, obj.l0, dt, hole)
                obj.r.append(r_temp)
                obj.r_p.append((obj.r[-1]-obj.r[-2])/dt)

                if obj.r[i]<1.5 or obj.r[i]>40:
                    obj.etat=0
                if obj.etat == 0 and obj == object.instances[0]:
                    stop = 1

        check_collision(object)

    return dt_array, stop