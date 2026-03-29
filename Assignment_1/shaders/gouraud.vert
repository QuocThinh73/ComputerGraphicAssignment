#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;
layout(location = 2) in vec3 normal;

uniform mat4 projection;
uniform mat4 modelview;

#define MAX_LIGHTS 4

uniform int num_lights;
uniform mat3 I_lights[MAX_LIGHTS];
uniform vec3 light_positions[MAX_LIGHTS];
uniform int light_enabled[MAX_LIGHTS];

uniform mat3 K_materials;
uniform float shininess;

out vec3 colorInterp;

void main() {
    vec4 vertPos4 = modelview * vec4(position, 1.0);
    vec3 vertPos = vec3(vertPos4) / vertPos4.w;

    mat4 normal_matrix = transpose(inverse(modelview));
    vec3 N = normalize(vec3(normal_matrix * vec4(normal, 0.0)));
    vec3 V = normalize(-vertPos);

    vec3 total_light_contribution = vec3(0.0);

    for(int i = 0; i < MAX_LIGHTS; i++) {
        if (i >= num_lights) break;
        if (light_enabled[i] == 0) continue;

        vec3 L = normalize(light_positions[i] - vertPos);
        vec3 R = reflect(-L, N);

        float specAngle = max(dot(R, V), 0.0);
        float specular = pow(specAngle, shininess);

        vec3 g = vec3(max(dot(L, N), 0.0), specular, 1.0);
        total_light_contribution += matrixCompMult(K_materials, I_lights[i]) * g;
    }

    vec3 rgb = 0.5 * total_light_contribution + 0.5 * color;
    colorInterp = rgb;

    gl_Position = projection * vertPos4;
}