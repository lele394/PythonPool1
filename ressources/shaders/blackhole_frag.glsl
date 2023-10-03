#version 330

out vec4 FragColor;

void main() {
    float dist = length(gl_PointCoord.xy - vec2(0.5));
    if (dist > 0.4) {
        discard;
    }
    FragColor = vec4(0.0, 0.0, 0.00, 1.0);
}
