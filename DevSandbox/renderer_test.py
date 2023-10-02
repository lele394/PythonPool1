# moderngl_window.run_window_config(App, args=["--window", "glfw"])
# ^ from here https://discord.com/channels/550302843777712148/550303654402588672/1157828847622950985

import PhysicsEngine as e





from array import array

import glm
import moderngl
import moderngl_window
from moderngl_window import geometry
from math import cos, sin, pi


class CircleRenderer:

    def __init__(self, ctx: moderngl.Context, program: moderngl.Program):
        self.ctx = ctx
        self.program = program
        self.capacity = 2


        self.position_data = array('f', [0.0] * 2 * self.capacity)
        self.position_buffer = self.ctx.buffer(data=self.position_data)
        # self.color_data = array('f', [1.0] * 3 * self.capacity)
        self.color_data = array('f', [1.0, 0.5, 0] * self.capacity)
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
        

        for i in range(self.capacity):
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

    def render(self):
        self.ctx.enable(moderngl.PROGRAM_POINT_SIZE)
        self.vao.render(moderngl.POINTS, self.capacity)















class BlackholeRenderer:

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bg_color = [33/255, 33/255, 33/255]
        self.fade_off = 0.01
        self.color_distance_treshold = 0.25


        self.blackhole_program = self.load_program(
            vertex_shader='blackhole_vert.glsl',
            fragment_shader='blackhole_frag.glsl',
        )

        self.circle_program = self.load_program(
            vertex_shader='circle_vert.glsl',
            fragment_shader='circle_frag.glsl',
        )

        self.circle_renderer = CircleRenderer(self.ctx, self.circle_program)

        self.blackhole_renderer = BlackholeRenderer(self.ctx, self.blackhole_program)
        self.blackhole_renderer.setup( )

        self.blit_program = self.load_program(
            vertex_shader='blit_vert.glsl',
            fragment_shader='blit_frag.glsl',
        )
        self.darken_program = self.load_program(
            vertex_shader='darken_vert.glsl',
            fragment_shader='darken_frag.glsl',
        )
        self.quad = geometry.quad_fs()

        self.fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture(self.wnd.size, components=4)],
        )

        self.blit_program["bg_color"] = self.bg_color
        self.blit_program["color_distance_treshold"] = self.color_distance_treshold

        self.darken_program["bg_color"] = self.bg_color
        self.darken_program["fade_off"] = self.fade_off


        # ! ================================
        self.theta = 0
        self.steps_per_frame = 2

        vel = 0.03


        self.bh = e.object("Blackhole", 0,0,0,0,10**12)

        self.projs = [
            e.object("Ship", 35, e.pi, 0, vel, 1, 1), #red
            # e.object("orange", 1.7, -1,  0, 10000000000,  1e80, 0.1), #blue
            # e.object("orange", 2, -1,  0, 5.7769,  1e80, 0.1), #blue
            e.object("Heavy", 35, 0, 0, -vel,  1, 1), #blue
        ]

        self.deltat = e.deltaless_deltat(self.projs)
        self.deltat = 0.1

        self.type_colors = {
            "red" : [1, 0, 0],
            "green": [0, 1, 0],
            "blue": [0, 0, 1],
            "cyan": [0, 1, 1],
            "pink": [1, 0, 1],
            "white":[1, 1, 1],
            "yellow": [1, 1, 0],
            "orange": [1, 0.5, 0],
            "neongreen": [0.31, 0.92, 1],
            "black": [0, 0, 0],

            "Ship": [0,1,0],
            "Heavy": [1, 0, 0],
            "Light": [0, 0, 1],
            "Target": [0.5, 1, 0]
        }





    def render(self, time, frame_time):


        self.ctx.clear()

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

        # r = 200
        # x = r * cos(self.theta) +self.window_size[0]/2
        # y = r * sin(self.theta) +self.window_size[1]/2
        # self.theta += 0.006
        # self.update_positions(x, y)


        (outs, self.projs, self.deltat, dt_list, col_list) = e.nbody_coupled_integrator(self.projs, self.bh, self.steps_per_frame, self.deltat)

        #make position list
        x_l = []
        y_l = []
        master_projs = self.projs + outs
        for i in range(len(master_projs)):

            obj = master_projs[i]

            r = obj.r
            theta = obj.theta


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
        self.update_positions_and_colors(x_l, y_l, col_l)







        #! end simulation shennanigans ===================================



        #render circles
        self.circle_renderer.render()


        # Blit framebuffer to screen
        self.ctx.screen.use()
        self.fbo.color_attachments[0].use(location=0)
        self.quad.render(self.blit_program)

        #render blackhole
        self.blackhole_renderer.render()

        if outs != []:
            input("huh oh")
        


    def update_positions_and_colors(self, x: list[float], y: list[float], colors: list[float]):
        
        positions = [0, 0] * len(x)
        for i in range(len(x)):
            positions[i * 2] = x[i]
            positions[i * 2 + 1] = y[i]

        # Move the circles
        self.circle_renderer.update(positions, colors)




moderngl_window.run_window_config(App)

