import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np

from libs.shader import *
from libs.buffer import *
from libs.lighting import LightingManager
from libs import transform as T


class FunctionGraph:
    def __init__(self, vert_shader, frag_shader):
        self.vert_shader = vert_shader
        self.frag_shader = frag_shader
        
        min_x = -5.0
        max_x = 5.0
        num_x = 200
        min_y = -5.0
        max_y = 5.0
        num_y = 200
        x_vals = np.linspace(min_x, max_x, num_x)
        y_vals = np.linspace(min_y, max_y, num_y)
        x_color_vals = np.linspace(0.0, 1.0, num_x)
        y_color_vals = np.linspace(0.0, 1.0, num_y)
        
        vertices = []
        colors = []
        
        for x in x_vals:
            for y in y_vals:
                z = np.sin(x) + np.cos(y)
                vertices.append([x, y, z])
                colors.append([(x_color_vals + y_color_vals) / 2] * 3)
                
        self.vertices = np.array(
            vertices,
            dtype=np.float32
        )
        
        self.colors = np.array(
            colors,
            dtype=np.float32
        )
        
        indices = []
        for i in range(num_x - 1):
            for j in range(num_y - 1):
                top_left = i * num_y + j
                top_right = top_left + 1
                bottom_left = (i + 1) * num_y + j
                bottom_right = bottom_left + 1
                
                indices.extend([top_left, top_right, bottom_left])
                indices.extend([top_right, bottom_right, bottom_left])
                
        self.indices = np.array(
            indices,
            dtype=np.int32
        )
        
        self.normals = self.vertices.copy()
        self.normals = self.normals / np.linalg.norm(self.normals, axis=1, keepdims=True)

        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        self.lighting = LightingManager(self.uma)

    def setup(self):
        # setup VAO for drawing cube
        self.vao.add_vbo(0, self.vertices, ncomponents=3, stride=0, offset=None)
        self.vao.add_vbo(1, self.colors, ncomponents=3, stride=0, offset=None)
        
        # Add normals for Gouraud/Phong shading (if shader needs it)
        if 'gouraud' in self.vert_shader.lower() or 'phong' in self.vert_shader.lower():
            self.vao.add_vbo(2, self.normals, ncomponents=3, stride=0, offset=None)

        # setup EBO
        self.vao.add_ebo(self.indices)

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
        
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.size, GL.GL_UNSIGNED_INT, None)
        
        self.vao.deactivate()
