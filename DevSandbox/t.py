import moderngl
import moderngl_window as mglw
import numpy as np

class MyWindow(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (800, 600)
    title = "Custom Vertex Shader with quad_fs Example"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load your texture (replace 'my_texture.png' with your texture file)


        red_color = np.array([255, 0, 0, 255], dtype=np.uint8)
        texture_data = np.tile(red_color, (800, 600, 1))



        self.texture = self.ctx.texture( (800, 600), 4, texture_data.tobytes())
        self.texture.build_mipmaps()

        # Create a shader prog
        self.prog = self.ctx.program(
            vertex_shader="""
                #version 330
                in vec2 in_vert;         // Vertex positions
                in vec2 in_texcoord;     // Texture coordinates
                out vec2 frag_texcoord;  // Output variable for passing texture coordinates to the fragment shader
                void main() {
                    gl_Position = vec4(in_vert, 0.0, 1.0);
                    frag_texcoord = in_texcoord;
                }
            """,
            fragment_shader="""
                #version 330
                uniform sampler2D tex;
                in vec2 frag_texcoord;
                out vec4 frag_color;
                void main() {
                    frag_color = texture(tex, frag_texcoord);
                }
            """
        )

        self.quad_vertices = np.array([
            -1.0, -1.0, 0.0, 1.0,  # Vertex positions (x, y) and texture coordinates (u, v)
            -1.0,  1.0, 0.0, 0.0,
             1.0, -1.0, 1.0, 1.0,
             1.0,  1.0, 1.0, 0.0,
        ], dtype='f4')

        # Create a full-screen quad with vertex attributes
        self.quad = self.ctx.simple_vertex_array(
    self.prog,
    self.ctx.buffer(self.quad_vertices),  # Provide your quad's vertex data
    'in_vert',              # Match shader attribute name
    'in_texcoord'           # Match shader attribute name
)

    def render(self, time, frame_time):
        self.ctx.clear()

        # Use the shader prog
        self.prog['tex'] = 0  # Bind texture to texture unit 0
        # self.prog.use()

        # Render the quad with the texture
        self.texture.use(location=0)  # Bind texture to texture unit 0
        self.quad.render(self.prog)

if __name__ == '__main__':
    MyWindow.run()
