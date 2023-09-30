#version 330

out vec4 fragColor;
uniform vec2 resolution;
uniform vec2 position;

float fadeoff = 0.80;

uniform sampler2D tex;

//============================================================
float circle(float radius, vec2 position)
{
  float value = distance(position , vec2(0.5));
  return step(radius, value);
}
//=============================================================

void main() {

  vec2 pixelCoord = gl_FragCoord.xy / resolution;

  float circleWidth = 1.0/600.0;

  float circle = circle(circleWidth, pixelCoord-position);

  vec4 prevColor = texture2D(tex, pixelCoord);

  if ( circle == 0.0)
  {
    fragColor = vec4(1.0);
  }
  else 
  {
    fragColor = vec4(0.047, 0.1333, 0.184, 0.5);
  }

  vec4 tex_color = texture(tex, pixelCoord);

  fragColor = fragColor + tex_color;

}