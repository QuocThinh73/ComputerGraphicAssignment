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
        
        self.num_points = 180
        self.base_radius = 0.9
        
        # vertices
        top_v = [[0, 0, +1]]
        bottom_v = [[0, 0, -1]]
        side_v = []
        # normals
        top_n = [[0, 0, 1]]
        bottom_n = [[0, 0, -1]]
        side_n = []
        # colors
        top_c = [[1.0, 0.0, 0.0]]
        bottom_c = [[0.0, 1.0, 0.0]]
        side_c = []
        
        for i in range(self.num_points + 1):
            angle_deg = 90 + i * (360 / self.num_points)
            angle_rad = np.radians(angle_deg)
            x = self.base_radius * np.cos(angle_rad)
            y = self.base_radius * np.sin(angle_rad)
            
            side_nx, side_ny = x / self.base_radius, y / self.base_radius
            
            # vertices
            top_v.append([x, y, +1])
            bottom_v.append([x, y, -1])
            side_v.extend([[x, y, 1], [x, y, -1]])
            # normals
            top_n.append([0, 0, 1])
            bottom_n.append([0, 0, -1])
            side_n.extend([[side_nx, side_ny, 0], [side_nx, side_ny, 0]])
            # colors
            top_c.append([0.0, 0.0, 1.0])
            bottom_c.append([1.0, 1.0, 0.0])
            side_c.extend([[0.0, 1.0, 1.0], [1.0, 0.0, 1.0]])
        
        self.vertices = np.array(
            top_v + bottom_v + side_v,
            dtype=np.float32
        )
        
        normals = np.array(
            top_n + bottom_n + side_n, 
            dtype=np.float32
        )
        self.normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)
        
        self.colors = np.array(
            top_c + bottom_c + side_c,
            dtype=np.float32
        )
        
        self.num_base_vertices = len(top_v)
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
        
        # top
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 0, self.num_base_vertices)
        # bottom
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, self.num_base_vertices, self.num_base_vertices)
        # side
        GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, self.num_base_vertices * 2, self.num_side_vertices)
        
        self.vao.deactivate()
