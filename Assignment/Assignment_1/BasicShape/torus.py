import numpy as np
import OpenGL.GL as GL

from libs.shader import *
from libs.buffer import *
from libs.lighting import LightingManager
from libs import transform as T


class Torus(object):
    def __init__(self, vert_shader, frag_shader):
        self.vert_shader = vert_shader
        self.frag_shader = frag_shader
        
        self.num_points = 180
        self.inner_radius = 0.75
        self.outer_radius = 1.5
        
        top_center = [0, 0, +1]
        bottom_center = [0, 0, -1]
        top_normal = [0, 0, 1]
        bottom_normal = [0, 0, -1]
        
        # vertices
        top_v = []
        bottom_v = []
        inner_v = []
        outer_v = []
        # normals
        top_n = []
        bottom_n = []
        inner_n = []
        outer_n = []
        # colors
        top_c = []
        bottom_c = []
        inner_c = []
        outer_c = []
        
        for i in range(self.num_points + 1):
            angle_deg = 90 + i * (360 / self.num_points)
            angle_rad = np.radians(angle_deg)
            cos_a = np.cos(angle_rad)
            sin_a = np.sin(angle_rad)
            inner_x = self.inner_radius * np.cos(angle_rad)
            inner_y = self.inner_radius * np.sin(angle_rad)
            outer_x = self.outer_radius * np.cos(angle_rad)
            outer_y = self.outer_radius * np.sin(angle_rad)
            
            inner_nx, inner_ny = inner_x / self.inner_radius, inner_y / self.inner_radius
            outer_nx, outer_ny = outer_x / self.outer_radius, outer_y / self.outer_radius
            
            # vertices
            top_v.extend([[inner_x, inner_y, +1], [outer_x, outer_y, +1]])
            bottom_v.extend([[inner_x, inner_y, -1], [outer_x, outer_y, -1]])
            inner_v.extend([[inner_x, inner_y, 1], [inner_x, inner_y, -1]])
            outer_v.extend([[outer_x, outer_y, 1], [outer_x, outer_y, -1]])
            # normals
            top_n.extend([[0, 0, 1], [0, 0, 1]])
            bottom_n.extend([[0, 0, -1], [0, 0, -1]])
            inner_n.extend([[-cos_a, -sin_a, 0], [-cos_a, -sin_a, 0]])
            outer_n.extend([[cos_a, sin_a, 0], [cos_a, sin_a, 0]])
            # colors
            top_c.extend([[0.0, 0.0, 1.0], [0.0, 0.0, 1.0]])
            bottom_c.extend([[1.0, 1.0, 0.0], [1.0, 1.0, 0.0]])
            inner_c.extend([[0.0, 1.0, 1.0], [0.0, 1.0, 1.0]])
            outer_c.extend([[1.0, 0.0, 1.0], [1.0, 0.0, 1.0]])
        
        self.vertices = np.array(
            top_v + bottom_v + inner_v + outer_v,
            dtype=np.float32
        )
        
        normals = np.array(
            top_n + bottom_n + inner_n + outer_n, 
            dtype=np.float32
        )
        self.normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)
        
        self.colors = np.array(
            top_c + bottom_c + inner_c + outer_c,
            dtype=np.float32
        )
        
        self.num_base_vertices = len(top_v)
        self.num_side_vertices = len(inner_v)

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
        GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, 0, self.num_base_vertices)
        # bottom
        GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, self.num_base_vertices, self.num_base_vertices)
        # inner
        GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, self.num_base_vertices * 2, self.num_side_vertices)
        # outer
        GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, self.num_base_vertices * 2 + self.num_side_vertices, self.num_side_vertices)
        
        self.vao.deactivate()
