#version 330

out vec4 FragColor;
uniform vec3 bg_color;
uniform float fade_off;

void main()
{
    FragColor = vec4(bg_color, fade_off);

    
    // if( distance(FragColor.rgb, bg_color) < 0.2)
    // {
    // }
    // else {

    //     FragColor = vec4(bg_color, 1);
    // }
        // FragColor = vec4(9/255, 32/255, 33/255, 0.01);
}
