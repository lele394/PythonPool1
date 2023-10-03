#version 330

in vec3 color;
out vec4 FragColor;

void main() {
    float dist = length(gl_PointCoord.xy - vec2(0.5));
    if (dist > 0.07) {
        discard;
    }
    FragColor = vec4(color, 1.0);
}
