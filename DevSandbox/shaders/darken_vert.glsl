#version 330

in vec3 in_position;

out vec2 uv;

void main() {
    gl_Position = vec4(in_position, 1.0);
}
