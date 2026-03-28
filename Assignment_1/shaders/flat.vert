#version 330 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_color;

out vec3 out_color;

uniform mat4 projection;
uniform mat4 modelview;

void main() {
    gl_Position = projection * modelview * vec4(in_position, 1.0);
    out_color = in_color;
}