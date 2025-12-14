#version 300 es
precision mediump float;
in vec2 v_texcoord;
uniform sampler2D tex;
out vec4 pixColor;

void main() {
    // Pixelate effect: 50x50 grid
    float size = 50.0;
    vec2 coord = floor(v_texcoord * size) / size;
    pixColor = texture(tex, coord);
}
