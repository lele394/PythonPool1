# moderngl_window.run_window_config(App, args=["--window", "glfw"])
# ^ from here https://discord.com/channels/550302843777712148/550303654402588672/1157828847622950985

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
        self.capacity = 1

        self.position_data = array('f', [0.0] * 2 * self.capacity)
        self.position_buffer = self.ctx.buffer(data=self.position_data)
        self.color_data = array('f', [1.0] * 3 * self.capacity)
        self.color_buffer = self.ctx.buffer(data=self.color_data)

        self.vao = self.ctx.vertex_array(
            self.program,
            [
                (self.position_buffer, '2f', 'in_vert'),
                (self.color_buffer, '3f', 'in_color'),
            ],
        )

    def update(self, time: float):
        """Update circle positions"""
        radius = 175.0 + sin(time) * 100.0

        for i in range(self.capacity):
            # Position data
            self.position_data[i * 2] = 300.0 + sin(time + 2*i/pi) * radius
            self.position_data[i * 2 + 1] = 300.0 + cos(time + 2*i/pi) * radius

            # Color data
            # self.color_data[i * 3] = 0.0
            # self.color_data[i * 3 + 1] = 2.0
            # self.color_data[i * 3 + 2] = 0.0

        self.position_buffer.write(self.position_data)

    def render(self):
        self.ctx.enable(moderngl.PROGRAM_POINT_SIZE)
        self.vao.render(moderngl.POINTS, self.capacity)


class App(moderngl_window.WindowConfig):
    window_size = 600, 600
    aspect_ratio = 1.0
    resource_dir = 'shaders'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.circle_program = self.load_program(
            vertex_shader='circle_vert.glsl',
            fragment_shader='circle_frag.glsl',
        )
        self.circle_renderer = CircleRenderer(self.ctx, self.circle_program)

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

    def set_uniform(self, u_name, u_value):
        try:
            self.prog[u_name] = u_value
        except KeyError:
            print(f'error at {u_name} = {u_value}')

    def render(self, time, frame_time):
        self.ctx.clear()

        # Set ortho projection
        self.circle_program["projection"].write(glm.ortho(
            0, self.wnd.width,
            0, self.wnd.height,
            -1, 1,
        ))
        # Move the circles
        self.circle_renderer.update(time*0.1)

        # Darken the previous frame
        self.fbo.use()
        self.ctx.enable(moderngl.BLEND)
        self.quad.render(self.darken_program)
        self.ctx.disable(moderngl.BLEND)
        self.circle_renderer.render()

        # Blit framebuffer to screen
        self.ctx.screen.use()
        self.fbo.color_attachments[0].use(location=0)
        self.quad.render(self.blit_program)



moderngl_window.run_window_config(App)
