#version 330

uniform sampler2D texture0;
in vec2 uv;
out vec4 FragColor;

void main()
{
    FragColor = texture(texture0, uv);
}
