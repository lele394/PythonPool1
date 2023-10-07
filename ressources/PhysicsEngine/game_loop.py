
from datetime import datetime
from .physicalConstants import *
from .engine_rev2 import *


def game_physics_loop(objects: list[object], 
                       blackhole: object, 
                       steps: int, 
                       initialDeltat: float
                       ):
    """
    main game loop.
    """
    # print(f'\n\n STARTING SIMULATION \n\n')
    

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
        if i %conf_statusPrintModulo == 0 and conf_statusDebug == True:
            print(f' {int(i/steps * 100)} % \t current deltat : {deltat:.5f} \t step time : {(datetime.now() - rem_time)} \t estimated remaining time : {(datetime.now() - rem_time) * (steps-i)}\t active objects {len(objects)}')
        rem_time = datetime.now()





        #resets depopulation indices
        objects_to_depop = []


        #quit if no objects are in the simulation.
        if len(objects) == 0:
            break
            



        # ~ Collision stuff hereeee
        # doNotUpdate = []
        col = []
        (objects, i, deltat, collision_iterations, col) = collisions(objects, i, deltat, collision_iterations, col)


        # * objects that shall not be updated as they already where in the collision
        # * don't need?
        # for pair in col:
        #     for i in pair:
        #         if  pair == "on grace": continue
        #         if objects[i] not in doNotUpdate:
        #             doNotUpdate.append(objects[i])





        #compute a deltat
        deltat = ComputeDeltatT(objects, deltat); deltat_list.append(deltat)
        # if i!=0 : deltat = ComputeDeltatT(objects, deltat); deltat_list.append(deltat)#do not run on first iteration, need to use deltat passed
        #for each object do 1 step
        for obj in objects:

            #debug objects
            # print(obj.r_list[-1] , "\t", obj.v_list[-1],"\t", obj.theta_list[-1], "\t", obj.speed_norm(deltat))


            #! uncomment
            # if obj in doNotUpdate: continue

            nbody_coupled_integrator(obj, blackhole, deltat)


            # print(obj.r_list[-1])
            # ~ escape conditions
            if obj.r_list[-1] < conf_outOfBoundMin or obj.r_list[-1] > conf_outOfBoundMax:


                if obj.r_list[-1] < conf_outOfBoundMin: print(f'object fell in blackhole, remaining objects before pop : {len(objects)}, iteration number {i}'); obj.IsOut = True
                if obj.r_list[-1] > conf_outOfBoundMax: print(f'object escape, remaining objects before pop : {len(objects)}, iteration number {i}'); obj.IsOut = True

                finished_objects.append(obj)

                objects_to_depop.append(obj)


        # * dels all specified objects to depop
        for obj_to_remove in objects_to_depop:
            objects.remove(obj_to_remove)
            print(f'depop {obj_to_remove}')


    # ~ makes sure everything has up to date variables
    # ^ this is here because when commenting the collision stuff to deactivate it,
    # ^ the renderer in opengl stops to work... It has an integrated update 
    for obj in objects:
        obj.UpdateVariables(deltat)
    for obj in finished_objects:
        obj.UpdateVariables(deltat)

    # * writes all remaining objects to the output list
    return (finished_objects, objects, deltat, deltat_list, collision_iterations, col)
    #                                   ^ deltat is returned cuz needed to initiate nextstep
    #                                                                              ^ col returned here to get the last collisions pair



