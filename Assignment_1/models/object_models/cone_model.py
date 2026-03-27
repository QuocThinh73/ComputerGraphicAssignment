import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class ConeModel(BaseModel):
    def __init__(self, vert_shader, frag_shader, radius, height):
        self.radius = radius
        self.height = height
        self.num_points = 360
        super().__init__(vert_shader, frag_shader)
        
    def _build_vertices(self):
        h = self.height / 2.0
        
        bottom_vertices = [
            [0, -h, 0] # bottom center
        ]
        side_vertices = [
            [0, +h, 0]
        ]
        
        for i in range(self.num_points + 1):
            angle = i * (2.0 * np.pi / self.num_points)
            x = self.radius * np.cos(angle)
            z = self.radius * np.sin(angle)
            
            bottom_vertices.append([x, -h, z])
            side_vertices.append([x, -h, z])
        
        self.vertices = np.array(
            bottom_vertices + side_vertices, 
            dtype=np.float32
        )
        
    def _build_colors(self):
        bottom_colors = [
            [1.0, 1.0, 1.0] # bottom center
        ]
        side_colors = [
            [1.0, 1.0, 1.0]
        ]
        
        for i in range(self.num_points + 1):
            angle = i * (2.0 * np.pi / self.num_points)
            
            r = np.cos(angle)
            g = np.sin(angle)
            b = 0.5 + 0.5 * np.cos(angle)
            
            bottom_colors.append([r, g, b])
            side_colors.append([r, g, b])
            
        self.colors = np.array(
            bottom_colors + side_colors,
            dtype=np.float32
        )
        
    def _draw_model(self):
        # bottom
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 0, len(self.vertices) // 2)
        # side
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, len(self.vertices) // 2, len(self.vertices) // 2)