import PhysicsEngine as e



import GameSettings as GS
from GameDisplay import *
from GameLogic import *
from utilities import clear_screen






class game():
    def __init__(self):
                # ! ================================

        # // change to include vars from GameSettings.py
        self.steps_per_frame = GS.steps_per_frame

        self.inventory = GS.starting_inventory

        
        # ^ SIMULATION VARIABLES HERE
        #black hole object, please don't touch the mass, projectiles speeds are balanced on it
        self.bh = e.object("Blackhole", 0,0,0,0,10**12)

        self.iteration = 0 #counter for the iteration number
        self.deltat_per_turn = 10

        self.counterdeltat = 0 #thing that counts the deltat spent since the last turn, needed as deltat changes
        self.masterCounterdeltat = 0


        (ship_vr, ship_vtheta, ship_r) = GameChoseStratShipPosition()
        #your initial projectiles, here just the ship and the target
        self.projs = [
            e.object("Ship", ship_r, e.pi, ship_vr, ship_vtheta, 1e5, 0.5), #red
            e.object("Target", 30, 0, 0, 0.05,  1e5, 0.5), #blue

            # ! debug
            # e.object("Ship", 30, e.pi, 0, -0.05, 1e5, 0.5), #red
            # e.object("Target", 30, 0, 0, 0.05,  2.5e4, 0.5), #blue

            
            
        ]

        self.deltat = e.deltaless_deltat(self.projs) #initialize the deltat for the first run

        self.type_colors = GS.color_table





    def game_loop(self):
                # * deltat shall not be calculated if its the 1st iteration
        self.deltat = e.ComputeDeltatT(self.projs, self.deltat);
        # if self.iteration != 0: self.deltat = e.ComputeDeltatT(self.projs, self.deltat);

        #increment the counter, however please note that the elapsed time between turns will not be exact each time
        # some errors are present that makes it so the deltat keeps on becoming smaller and smaller.
        # we decide to stop once the counter goes above a threshold, see next if
        self.counterdeltat += self.deltat
        self.masterCounterdeltat += self.deltat


        # ! that's the run simulation function, and one hell of a thing to implement
        (outs, self.projs, self.deltat, dt_list, col_list, col_pairs) = e.game_physics_loop(self.projs, self.bh, self.steps_per_frame, self.deltat)

        explosions_locations = [] # for potential future rendering of collisions

        #check for gamerules collisions
        GameruleCollisions(self, col_pairs, explosions_locations)        

        # * OUT OF BOUND CHECKS ============================================================

        #check if the ship or the target are in the out lists, which would mean they fell in the black hole
        for obj in outs:
            if obj.type == "Ship":
                GameLoss("FIBH")
            elif obj.type == "Target":
                GameWin("FIBH")

        #ship id is always 0 since it's instanciated first
        ship = self.projs[0]
        #target id is always 1 since it's instanciated in second
        target = self.projs[1]
        #first check for the ship state. useles to check further if the ship is already out
        # gotta make sure that we don't ccidentally trigger an out of bound when the periodic boundary condition is active
        if ship.r > GS.out_of_bound and not(GS.periodic_boundary_condition_is_active):
            GameLoss("OOB")
        
        if target.r > GS.out_of_bound and not(GS.periodic_boundary_condition_is_active):
            GameWin("OOB", self.masterCounterdeltat)


        #check for all objects that may leave the lay area
        for obj in self.projs:
            if obj.r > GS.out_of_bound:
                #if we're using the periodic boundary condition
                if GS.periodic_boundary_condition_is_active:

                    #spin it around
                    # we can just multiply by deltat since we're far from the blackhole; 1st order corrections are not applicable
                    obj.theta = obj.theta + e.pi #spin theta by pi
                    obj.theta_list.append(obj.theta)
                    obj.vr = -obj.vr# radial speed must be inversed
                    obj.v_list.append(obj.vr) # add the newly inversed speed

                    obj.r = GS.out_of_bound # gotta bring back the ball in the play area
                    obj.r_list.append(obj.r )

                #and remove then if they're too far
                else: self.projs.remove(obj)


        #* ================================================================================





        # * turn loop with input management
        if self.counterdeltat >= self.deltat_per_turn: # if enough time has passed since the last turn
            clear_screen()

            # prints info of all the available objects 
            # in the simulation.
            #  quick and dirty but works
            for i in self.projs:
                i.Debug(self.deltat)


            print(f'time elapsed since last turn {self.counterdeltat}, deltat {self.deltat}, game time {self.masterCounterdeltat}')
            self.counterdeltat = 0 # resets the counter for the next turn
            inp = GameNewTurn()#display new turn screen

            if inp =="q":
                quit()






            if inp == "l":
                
                to_add = [] # list to keep the coordinates of the new object
                while inp != "c" or inp !="cancel":
                    #checks that there are remaining missiles
                    if self.inventory["Heavy"] + self.inventory["Light"] <= 0:
                        OutOfEveryting()
                        break

                    if inp == "c" or inp == "cancel": break#escape condiion for firing confirmation

                    #make sure it's formatted correctly
                    formatted_correctly = False
                    while not formatted_correctly:
                        inp = GameFiring(self.inventory)
                        inp_split = [i for i in inp.split(" ")]
                        try:
                            float(inp_split[0]) # makes sure the first item can be interpreted as a float
                            #makes sure the 2nd item is a valid type
                            if any(char in inp_split[1] for char in ('h', 'H', 'heavy', 'Heavy', 'l', 'L', 'light', 'Light')):
                                formatted_correctly = True
                        except:
                            print("\033[92mcommand\033[91m@firing-console\033[95m ! formatting does not seem correct, did you mistype something?\033[97m  ")


                    projectile_type = ProjectileMatch(self, inp_split)

                    if projectile_type != None:
                        (inp, vr, vt, projectile) = Shoot(inp_split, projectile_type)
                if inp == "c": # confims launch
                    #creates the bullet
                    CreateMissile(self, vr, vt, projectile_type, ship, projectile, self.deltat)





# game start thingy
while True:
    #display game banner
    GameBanner()

    #gets input from the menu
    inp = GameMenu()

    if any(char in inp for char in ('p', 'P', '1')):
        skip = False
        #plays the game introduction or not if you want to skip it
        inp = input("Do you wish to (s)kip the intro?(enter twice to see it)\n > ")
        if any(char in inp for char in ('s', 'S')): skip = True
        GameIntroduction(skip)
        

        #start game here
        g = game()
        while True:# non stop loop 
            g.game_loop()


        pass

    elif any(char in inp for char in ('h', 'H', '2')):
        #print help
        GameHowToPlay()

    elif any(char in inp for char in ('c', 'C', '3')):
        GameCredits()

    elif any(char in inp for char in ('q', 'Q', '4')):
        quit()

