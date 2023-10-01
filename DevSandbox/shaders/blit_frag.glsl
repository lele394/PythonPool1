#version 330

uniform sampler2D texture0;
uniform vec3 bg_color;
uniform float color_distance_treshold;
in vec2 uv;
out vec4 FragColor;

void main()
{
    FragColor = texture(texture0, uv);
    if( distance(FragColor.rgb, bg_color) < color_distance_treshold)
    {
        FragColor = vec4(bg_color, 1);
    }
}
