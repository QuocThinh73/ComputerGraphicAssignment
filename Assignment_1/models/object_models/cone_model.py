import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class ConeModel(BaseModel):
    def __init__(self, vert_shader, frag_shader, radius, height, color):
        self.radius = radius
        self.height = height
        self.num_points = 360
        self.color = color
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
        
    def _build_normals(self):
        bottom_count = len(self.vertices) // 2
        bottom_normals = np.tile([0.0, -1.0, 0.0], (bottom_count, 1))
        
        side_normals = [
            [0.0, 1.0, 0.0]
        ]
        
        len_n = np.sqrt(self.height**2 + self.radius**2) 
        ny = self.radius / len_n
        
        for i in range(self.num_points + 1):
            angle = i * (2.0 * np.pi / self.num_points)
            
            nx = (self.height * np.cos(angle)) / len_n
            nz = (self.height * np.sin(angle)) / len_n
            
            side_normals.append([nx, ny, nz])
            
        self.normals = np.vstack((bottom_normals, side_normals)).astype(np.float32)
        
    def _build_colors(self):
        shader_name = self.vert_shader.lower()
        if 'gouraud' in shader_name or 'phong' in shader_name:
            self.colors = np.zeros_like(self.vertices, dtype=np.float32)
        elif 'flat' in shader_name:
            self.colors = np.tile(self.color, (len(self.vertices), 1)).astype(np.float32)
        else:
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