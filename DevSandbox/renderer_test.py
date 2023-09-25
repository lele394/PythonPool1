import moderngl_window as mglw
import PhysicsEngine.test as PE


class Test(mglw.WindowConfig):
    gl_version = (3, 3)

    def render(self, time, frametime):
        self.ctx.clear(1.0, 0.0, 1.0, 0.0)

Test.run()

