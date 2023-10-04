from GameDisplay import *
import GameSettings as GS
import PhysicsEngine as e
import numpy as np
from math import cos, sin
from PhysicsEngine import pi




def addCoordinatesToList(l, a, b):
    l.append(
        (
            a.r, a.theta,
            b.r, b.theta
        )
    )






def ProjectileMatch(self, inp_split):
    ship_id = 0 #should always be 0
    ship = self.projs[ship_id]

    projectile_type = ""
    #match the right projectile type to the entry
    match str(inp_split[1]):
        case "h" | "H" | "Heavy" | "heavy":
            if self.inventory["Heavy"] > 0:
                projectile_type = "Heavy"
                self.inventory["Heavy"] -= 1
            else:
                OutOfAmmo("Heavy")
                projectile_type = None

        case "l" | "L" | "Light" | "light":
            if self.inventory["Light"] > 0:
                projectile_type = "Light"
                self.inventory["Light"] -= 1
            else:
                OutOfAmmo("Light")
                projectile_type = None

        case _:
            print("error parsing the projectile type, that shouldn't be possible, escaping")
            input("quit... ")
            quit()
    return projectile_type










def Shoot(inp_split, projectile_type):
    firing_angle = float(inp_split[0]) * pi / 180
    projectile = GS.projectiles_default[projectile_type]

    #calculates components of v
    vr = projectile["speed"] * -sin(firing_angle) # minus on the sinus to make it more intuitive, counter clockwise shooting
    vt = projectile["speed"] * cos(firing_angle)  # we're firing "towards" the black hole

    print(f'\033[92mcommand\033[91m@firing-console\033[95m ! Will launch a projectile of speed : angle {round(firing_angle, 4)}rad\t vtheta {round(vt, 4)}\t vr {round(vr, 4)}')

    inp = input("\033[92mcommand\033[91m@firing-console\033[95m ! (c)onfirm or (cancel)\n\033[92mcommand\033[91m@firing-console\033[97m> ")

    return inp, vr, vt, projectile





def CreateMissile(self, vr, vt, projectile_type, ship, projectile, deltat):
    print(f'ship vars {vr, vt}')
    bullet = e.object(projectile_type, ship.r, ship.theta, ship.vr + vr, ship.vtheta+vt, projectile["mass"], projectile["radius"])

    # bullet = e.object(projectile_type, ship.r, ship.theta, ship.vr, ship.vtheta, projectile["mass"], projectile["radius"])

    #adds the ship as an initial object it's colliding with
    bullet.WasColliding.append(ship)
    bullet.WasColliding.append("SpawnedOnShip")#check for collisions on summon


    #! SHENNNIGANS, VR SEEMS WRONG IN SIM

    e.nbody_coupled_integrator(bullet, e.object("Blackhole", 0,0,0,0,10**12), deltat)

    bullet.UpdateVariables(deltat)
    #adds the bullet into the simulation
    self.projs.append(
        bullet
        )





def GameruleCollisions(self, col_pairs, explosions_locations):
    for pair in col_pairs:
        print(pair)
        a = self.projs[pair[0]]
        b = self.projs[pair[1]]

        # ! GAME LOGIC ====================================================================
        # * please refer to GameSettings.py for the truthtable
        match a.type:
            case "Heavy":
                match b.type:
                    case "Light":
                        #destroy both objects by removing them of the simulation
                        addCoordinatesToList(explosions_locations, a, b)
                        self.projs.remove(a)
                        self.projs.remove(b)
                    
                    case "Heavy" | "Ship" | "Target":
                        ElasticCollision()

                    case _:#undetermined case
                        print(f'could not determine the type of collision for {(a.type, b.type)}, are you using debug colors as types?')

            case "Light":
                match b.type:
                    case "Light":
                        #destroy both objects by removing them of the simulation
                        addCoordinatesToList(explosions_locations, a, b)  
                        self.projs.remove(a)
                        self.projs.remove(b)

                    case "Heavy":
                        #destroy both objects by removing them of the simulation
                        addCoordinatesToList(explosions_locations, a, b)    
                        self.projs.remove(a)
                        self.projs.remove(b)

                    case "Target":
                        GameWin("LT", self.masterCounterdeltat)  

                    case "Ship":
                        if "SpawnedOnShip" in b.WasColliding:GameLoss("LS") 

                    case _: #undetermined case
                        print(f'could not determine the type of collision for {(a.type, b.type)}, are you using debug colors as types?')

            case "Target":
                match b.type:
                    case "Light":
                        GameWin("LT", self.masterCounterdeltat)

                    case "Ship":
                        GameWin("TS", self.masterCounterdeltat)

                    case "Heavy":
                        ElasticCollision()

                    case _: #undetermined case
                        print(f'could not determine the type of collision for {(a.type, b.type)}, are you using debug colors as types?')

            case "Ship":
                match b.type:
                    case "Light":
                        if b in a.WasColliding:
                            GameLoss("LS")

                    case "Target":
                        GameWin("TS", self.masterCounterdeltat)

                    case "Heavy":
                        ElasticCollision()
                        
                    case _: #undetermined case
                        print(f'could not determine the type of collision for {(a.type, b.type)}, are you using debug colors as types?')


            case _: #undetermined case
                print(f'could not determine the type of collision for {(a.type, b.type)}, are you using debug colors as types?')
        # ! ================================================================================








