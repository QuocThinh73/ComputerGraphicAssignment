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
        
        self.num_sectors = 180
        big_circle_radius = 1.0
        self.num_sides = 180
        small_circle_radius = 0.3
        
        vertices = []
        colors = []
        
        for i in range(self.num_sectors):
            theta1 = 90 + i * (360 / self.num_sectors)
            theta1 = np.radians(theta1)
            
            theta2 = 90 + (i + 1) * (360 / self.num_sectors)
            theta2 = np.radians(theta2)
            
            for j in range(self.num_sides):
                phi1 = 90 + j * (360 / self.num_sides)
                phi1 = np.radians(phi1)
                
                phi2 = 90 + (j + 1) * (360 / self.num_sides)
                phi2 = np.radians(phi2)
                
                x11 = (big_circle_radius + small_circle_radius * np.cos(phi1)) * np.cos(theta1)
                y11 = (big_circle_radius + small_circle_radius * np.cos(phi1)) * np.sin(theta1)
                z11 = small_circle_radius * np.sin(phi1)
                
                x12 = (big_circle_radius + small_circle_radius * np.cos(phi1)) * np.cos(theta2)
                y12 = (big_circle_radius + small_circle_radius * np.cos(phi1)) * np.sin(theta2)
                z12 = small_circle_radius * np.sin(phi1)
                
                x21 = (big_circle_radius + small_circle_radius * np.cos(phi2)) * np.cos(theta1)
                y21 = (big_circle_radius + small_circle_radius * np.cos(phi2)) * np.sin(theta1)
                z21 = small_circle_radius * np.sin(phi2)
                
                x22 = (big_circle_radius + small_circle_radius * np.cos(phi2)) * np.cos(theta2)
                y22 = (big_circle_radius + small_circle_radius * np.cos(phi2)) * np.sin(theta2)
                z22 = small_circle_radius * np.sin(phi2)
                
                vertices.extend([x11, y11, z11, x12, y12, z12, x21, y21, z21])
                vertices.extend([x12, y12, z12, x22, y22, z22, x21, y21, z21])
                colors.extend([1.0, 0.0, 0.0] * 18)
        
        self.vertices = np.array(
            vertices,
            dtype=np.float32
        )
        
        self.normals = self.vertices.copy()
        # self.normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)
        
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
        
        # top
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self.vertices))
        
        self.vao.deactivate()
