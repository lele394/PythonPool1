#version 330

uniform mat4 projection;
in vec2 in_vert;
in vec3 in_color;

out vec3 color;

void main() {
    gl_Position = projection * vec4(in_vert, 0.0, 1.0);
    color = in_color;
    gl_PointSize = 40.0;
}
