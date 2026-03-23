import numpy as np
import OpenGL.GL as GL

from libs.shader import *
from libs.buffer import *
from libs.lighting import LightingManager
from libs import transform as T


class Cylinder(object):
    def __init__(self, vert_shader, frag_shader):
        self.vert_shader = vert_shader
        self.frag_shader = frag_shader
        
        base_num_points = 180
        base_radius = 0.9
        base_vertices = [
            [[0, 0, +1]],     # upper_base_center
            [[0, 0, -1]]      # lower_base_center
        ]  
        
        for i, base_center in enumerate(base_vertices):
            for j in range(base_num_points + 1):
                angle_deg = 90 + j * (360 / base_num_points)
                angle_rad = np.radians(angle_deg)
                x = base_radius * np.cos(angle_rad)
                y = base_radius * np.sin(angle_rad)
                base_vertices[i].append([x, y, base_center[0][2]])
        
        self.vertices = np.array(
            base_vertices, 
            dtype=np.float32
        )
        
        normals = np.random.normal(0, 3, (len(self.vertices), 3)).astype(np.float32)
        normals[:, 2] = np.abs(normals[:, 2])
        self.normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)

        # colors: RGB format
        colors = [
            [[1.0, 0.0, 0.0]],    # upper_base_center
            [[0.0, 1.0, 0.0]]     # lower_base_center
        ]
        
        for i in range(len(colors)):
            for _ in range(base_num_points + 1):
                colors[i].append([0.0, 0.0, 1.0])
        
        self.colors = np.array(
            colors,
            dtype=np.float32
        )

        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        self.lighting = LightingManager(self.uma)

    def setup(self):
        self.vao.add_vbo(0, self.vertices, ncomponents=3, stride=0, offset=None)
        self.vao.add_vbo(1, self.colors, ncomponents=3, stride=0, offset=None)
        
        # Add normals for Gouraud/Phong shading (if shader needs it)
        if 'gouraud' in self.vert_shader.lower() or 'phong' in self.vert_shader.lower():
            self.vao.add_vbo(2, self.normals, ncomponents=3, stride=0, offset=None)
            
        return self

    def draw(self, projection, view, model):
        GL.glUseProgram(self.shader.render_idx)
        modelview = view

        self.uma.upload_uniform_matrix4fv(projection, 'projection', True)
        self.uma.upload_uniform_matrix4fv(modelview, 'modelview', True)
        
        # Setup lighting if using Gouraud or Phong shader
        if 'gouraud' in self.vert_shader.lower():
            self.lighting.setup_gouraud()
        elif 'phong' in self.vert_shader.lower():
            self.lighting.setup_phong(mode=1)
        
        self.vao.activate()
        
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 0, len(self.vertices[0]))
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 0, len(self.vertices[1]))
        self.vao.deactivate()
