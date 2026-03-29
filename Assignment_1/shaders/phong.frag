#version 330 core

precision mediump float;
in vec3 normal_interp;  
in vec3 vertPos;       
in vec3 colorInterp;

uniform mat3 K_materials;
uniform int mode;   
uniform float shininess; 

#define MAX_LIGHTS 4

uniform int num_lights;
uniform mat3 I_lights[MAX_LIGHTS];
uniform vec3 light_positions[MAX_LIGHTS];
uniform int light_enabled[MAX_LIGHTS];

out vec4 fragColor;

void main() {
  vec3 N = normalize(normal_interp);
  vec3 V = normalize(-vertPos); 

  vec3 total_light_contribution = vec3(0.0);

  for (int i = 0; i < MAX_LIGHTS; i++) {
      if (i >= num_lights) break;
      if (light_enabled[i] == 0) continue;

      vec3 L = normalize(light_positions[i] - vertPos);
      vec3 R = reflect(-L, N);      

      float specAngle = max(dot(R, V), 0.0);
      float specular = pow(specAngle, shininess);
      vec3 g = vec3(max(dot(L, N), 0.0), specular, 1.0);
      
      total_light_contribution += matrixCompMult(K_materials, I_lights[i]) * g;
  }

  vec3 rgb = 0.5 * total_light_contribution + 0.5 * colorInterp;

  fragColor = vec4(rgb, 1.0);
}