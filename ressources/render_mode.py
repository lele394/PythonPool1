# moderngl_window.run_window_config(App, args=["--window", "glfw"])
# ^ from here https://discord.com/channels/550302843777712148/550303654402588672/1157828847622950985

import PhysicsEngine as e



import GameSettings as GS
from GameDisplay import *
from GameLogic import *
from utilities import clear_screen



from array import array

import glm
import moderngl
import moderngl_window
from moderngl_window import geometry
from math import cos, sin


class CircleRenderer:

    def __init__(self, ctx: moderngl.Context, program: moderngl.Program):
        """
        einarf moderngl wizardry, creates position and color buffers
        to render the circles representing objects in the simulation.
        
        Thanks a lot to Einar Forselv for the help in implementing 
        the render circle and general knowledge about moderngl and mglw
        
        """
        self.ctx = ctx
        self.program = program
        self.max_capacity = 10000 # max number of circles

        # * buffers initializations with the max capacity
        self.position_data = array('f', [0.0] * 2 * self.max_capacity)
        self.position_buffer = self.ctx.buffer(data=self.position_data)
        # self.color_data = array('f', [1.0] * 3 * self.capacity)
        self.color_data = array('f', [1.0, 0.5, 0] * self.max_capacity)
        self.color_buffer = self.ctx.buffer(data=self.color_data)

        self.vao = self.ctx.vertex_array(
            self.program,
            [
                (self.position_buffer, '2f', 'in_vert'),
                (self.color_buffer, '3f', 'in_color'),
            ],
        )





    def update(self, positions, colors ):
        """Update circle positions"""
        

        for i in range(int(len(positions) / 2)): # x and y for positions so divide by 2
            """
            position_data = [x1, y1, x2, y2, ..., xn, yn]
            color_data = [r1, g1, b1, r2, g2, b2, ..., rn, gn, bn]

            """
            # Position data

            self.position_data[i * 2] = positions[i * 2]
            self.position_data[i * 2 + 1] = positions[ i * 2 + 1]

            # Color data
            self.color_data[i * 3] = colors[i*3]
            self.color_data[i * 3 + 1] = colors[i*3 + 1]
            self.color_data[i * 3 + 2] = colors[i*3 + 2]

        self.position_buffer.write(self.position_data)
        self.color_buffer.write(self.color_data)

    def render(self, number_of_circles):
        self.ctx.enable(moderngl.PROGRAM_POINT_SIZE)
        self.vao.render(moderngl.POINTS, number_of_circles)















class BlackholeRenderer:
    """pretty much the same as the circle renderer except it only is for the blackhole"""
    def __init__(self, ctx: moderngl.Context, program: moderngl.Program):
        self.ctx = ctx
        self.program = program
        self.capacity = 1


        self.position_data = array('f', [0, 0])
        self.position_buffer = self.ctx.buffer(data=self.position_data)
        # self.color_data = array('f', [1.0] * 3 * self.capacity)
        self.color_data = array('f', [1.0, 1.0, 1.0])
        self.color_buffer = self.ctx.buffer(data=self.color_data)

        self.vao = self.ctx.vertex_array(
            self.program,
            [
                (self.position_buffer, '2f', 'in_vert'),
                (self.color_buffer, '3f', 'in_color'),
            ],
        )

    def setup(self):
        """setup blackhole"""


        self.position_buffer.write(self.position_data)
        self.color_buffer.write(self.color_data)

    def render(self):
        self.ctx.enable(moderngl.PROGRAM_POINT_SIZE)
        self.vao.render(moderngl.POINTS, self.capacity)










class App(moderngl_window.WindowConfig):
    window_size = 900, 900
    aspect_ratio = 1.0
    resource_dir = 'shaders'

    def __init__(self,**kwargs):
        """
        initialisation of the window, and all the rest
        """


        super().__init__(**kwargs)

        # * aesthetics~~ colors and stuff, customize to make it look CoOoOoLlLl
        self.bg_color = GS.background_color
        self.fade_off = GS.fade_off
        self.color_distance_treshold = GS.color_distance_treshold
        """
        carefull, background color is implemented in fade off, making it a bad 
        idea as it does not have its own display shader. the distance between colors is 
        therefore *extremely* broken
        # todo custom background shader


        maybe starry background? oopsies
        idea :
            just put some random dots every now and then in one frame, they'll fade with the 
            darken shader
        
        """



        # ! creating shader programs =====================================
        self.blackhole_program = self.load_program(
            vertex_shader='blackhole_vert.glsl',
            fragment_shader='blackhole_frag.glsl',
        )

        self.circle_program = self.load_program(
            vertex_shader='circle_vert.glsl',
            fragment_shader='circle_frag.glsl',
        )

        self.blit_program = self.load_program(
            vertex_shader='blit_vert.glsl',
            fragment_shader='blit_frag.glsl',
        )
        self.darken_program = self.load_program(
            vertex_shader='darken_vert.glsl',
            fragment_shader='darken_frag.glsl',
        )
        # ! ==============================================================


        # * setting up shaders uniforms, renderers and display geometry
        # ~ blit 
        self.blit_program["bg_color"] = self.bg_color
        self.blit_program["fade_off"] = self.fade_off
        self.blit_program["color_distance_treshold"] = self.color_distance_treshold

        # ~ darkener
        self.darken_program["bg_color"] = self.bg_color
        self.darken_program["fade_off"] = self.fade_off

        # ~ renderers setup
        self.circle_renderer = CircleRenderer(self.ctx, self.circle_program)

        self.blackhole_renderer = BlackholeRenderer(self.ctx, self.blackhole_program)
        self.blackhole_renderer.setup( )

        # ~ display quad geometry
        self.quad = geometry.quad_fs()

        self.fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture(self.wnd.size, components=4)],
        )
        # * ======================================================

        # ! ================================

        # todo change to include vars from GameSettings.py
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





    def render(self, time, frame_time):


        self.ctx.clear() # clears previous image

        # Set ortho projection for circles
        self.circle_program["projection"].write(glm.ortho(
            0, self.wnd.width,
            0, self.wnd.height,
            -1, 1,
        ))




        # Darken the previous frame
        self.fbo.use()
        self.ctx.enable(moderngl.BLEND)
        self.quad.render(self.darken_program)
        self.ctx.disable(moderngl.BLEND)

        #! simulation shennanigans =======================================

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






        # & from here we're converting object positions to cartesian 
        # & so it can be understood by the shader.
        # & could probably pass it in and parallelize it, but oh well
        # & it ain't that heavy *yet*
        #make position list
        x_l = []
        y_l = []
        master_projs = self.projs + outs

        number_of_circles = len(master_projs)


        for i in range(len(master_projs)):

            obj = master_projs[i]

            r = obj.r
            theta = obj.theta

            #10 zoom factor of the gamespace
            x = r*10 * cos(theta) +self.window_size[0]/2
            y = r*10 * sin(theta) +self.window_size[1]/2

            x_l.append(x)
            y_l.append(y)



        #make color list
        col_l = []
        for obj in master_projs:
            col = self.type_colors[obj.type]
            col_l = col_l + col


        #update colors and positions
        self.update_positions_and_colors(x_l, y_l, col_l, number_of_circles)


        #! end simulation shennanigans ===================================



        # *displaying STUFF ========================================

        #render circles
        self.circle_renderer.render(number_of_circles)


        # Blit framebuffer to screen
        self.ctx.screen.use()
        self.fbo.color_attachments[0].use(location=0)
        self.quad.render(self.blit_program)

        #render blackhole
        self.blackhole_renderer.render()
        # * =========================================================
        
        # debug breakout when collisions happen. leaving it here
        # cuz might need it if i add some explosion stuff
        #like 2D pew pew with circles around collision points
        # ah well tht'd be another shder but y not

        # if outs != []:
        #     input("huh oh")
        


    def update_positions_and_colors(self, x: list[float], y: list[float], colors: list[float], number_of_circles: int):
        """creates positions list tht fit in the sahder buffer"""
        positions = [0, 0] * len(x)
        for i in range(len(x)):
            positions[i * 2] = x[i]
            positions[i * 2 + 1] = y[i]

        # Move the circles
        self.circle_renderer.update(positions, colors)













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
        moderngl_window.run_window_config(App)
        pass

    elif any(char in inp for char in ('h', 'H', '2')):
        #print help
        GameHowToPlay()

    elif any(char in inp for char in ('c', 'C', '3')):
        GameCredits()

    elif any(char in inp for char in ('q', 'Q', '4')):
        quit()




# do something about credits or something
# lil menu, yk the drill
# start game and input velcoity should be put here aswell


inp = input(" > ")




# some stuff to do :
#       ! ESCAPE VELOCITY COMPARISON IN OOB # no time
#   //    ! PROJECTILE LUNCH ANGLE
#  //     ! PLAYER SET STARTING RADIUS AND VECTOR
#     //well there's the thing about setting defult values to projectiles
#     //and default config to start a game

#    //DONE   s OUT OF BOUND IS NOT IMPLEMENTED YET 

#     //#~pretty well into that story telling and all, needa do the win texts

#     todo also the damn copy paste of everything here as a console thingy
    # prob just gonna print the shit out of object.debug to the console

    # let's do the report first tho nope no time also recoil and  #// done actually out of bound comebacks maybe

    # // todo inventory for the number of missiles fired

    # inelastic collisions and debris could be fun, but need to pass a radius
    # to the shader sooooooo...................

    # todo testing if all exit conditions work? #out of time

    # ayyyyyyyy polar reticle could be quite funny #i wishhhhh maybe in the weekend? shouldn't be too long

    #//check variables that can be put in the config file

    # //START REPORT??????? O:)

    # ! start.sh and setup #bash if function for graphical or console mode once it's done













# ! PART3 test stuff
# ! CMD EDITION PLEAAAASE


# moderngl_window.run_window_config(App)

