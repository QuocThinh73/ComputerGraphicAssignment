import numpy as np
import OpenGL.GL as GL

from libs.shader import *
from libs.buffer import *
from libs.lighting import LightingManager
from libs import transform as T


class Cone(object):
    def __init__(self, vert_shader, frag_shader):
        self.vert_shader = vert_shader
        self.frag_shader = frag_shader
        
        self.num_points = 180
        self.base_radius = 0.9
        
        # vertices
        base_v = [[0, 0, -1]]
        side_v = [[0, 0, +1]]
        # normals
        base_n = [[0, 0, -1]]
        side_n = [[0, 0, +1]]
        # colors
        base_c = [[1.0, 0.0, 0.0]]
        side_c = [[0.0, 1.0, 0.0]]
        
        for i in range(self.num_points + 1):
            angle_deg = 90 + i * (360 / self.num_points)
            angle_rad = np.radians(angle_deg)
            x = self.base_radius * np.cos(angle_rad)
            y = self.base_radius * np.sin(angle_rad)
            
            side_nx, side_ny = x / self.base_radius, y / self.base_radius
            
            # vertices
            base_v.append([x, y, -1])
            side_v.append([x, y, -1])
            # normals
            base_n.append([0, 0, -1])
            side_n.append([side_nx, side_ny, 0])
            # colors
            base_c.append([0.0, 0.0, 1.0])
            side_c.append([0.0, 1.0, 1.0])
        
        self.vertices = np.array(
            base_v + side_v,
            dtype=np.float32
        )
        
        normals = np.array(
            base_n + side_n, 
            dtype=np.float32
        )
        self.normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)
        
        self.colors = np.array(
            base_c + side_c,
            dtype=np.float32
        )
        
        self.num_base_vertices = len(base_v)
        self.num_side_vertices = len(side_v)

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
        
        # base
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 0, self.num_base_vertices)
        # side
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, self.num_base_vertices, self.num_side_vertices)
        
        self.vao.deactivate()
