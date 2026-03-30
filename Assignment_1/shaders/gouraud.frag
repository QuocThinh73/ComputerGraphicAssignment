#version 330 core

precision mediump float;

in vec3 colorInterp;

out vec4 fragColor;

void main() {
    fragColor = vec4(colorInterp, 1.0);
}