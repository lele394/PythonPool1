import moderngl_window as mglw
import PhysicsEngine.engine as e
from math import cos, sin


















class App(mglw.WindowConfig):
    window_size = 600,600
    resource_dir = 'shaders'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.quad = mglw.geometry.quad_fs()

        self.prog = self.load_program(vertex_shader = 'vertex.glsl', fragment_shader='fragment.glsl')

        self.set_uniform('resolution', self.window_size)


        #assign texture to channel 0
        #self.prog['tex'] = 0
        



        self.zoom = 0.01
        #simu
        self.deltat = 1

        self.bh = e.object(0,0,0,0,10**10)
        self.proj = e.object(15, 0, 0, 0.007, 1000)
        #for proj
        self.l0_proj = e.compute_l0(self.proj.r, self.proj.vtheta)
        self.theta = 0
        self.r = []


        self.fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture((self.window_size), 4, dtype="f1")],
        )






    def set_uniform(self, u_name, u_value):
        try:
            self.prog[u_name] = u_value
        except:
            print(f'error at {u_name} = {u_value}')



    def render(self, time, frame_time):
        self.ctx.clear()

        #https://discord.com/channels/550302843777712148/550303654402588672/1156002515742117888
        #self.fbo.use()
        #self.fbo.color_attachments[0].use()


        r = e.Leapfrog_integrator(self.proj, self.bh, 2, self.l0_proj, self.deltat)[0][-1]
        self.theta = e.theta_next(self.theta, self.l0_proj, r, self.deltat)

        x = r*cos(self.theta)
        y = r*sin(self.theta)

        pos = (x*self.zoom,y*self.zoom)
        #print(pos)



        self.set_uniform('position', pos)

        self.quad.render(self.prog)


mglw.run_window_config(App)