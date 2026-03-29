import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class TruncatedConeModel(BaseModel):
    def __init__(self, bottom_radius, top_radius, height, **kwargs):
        self.bottom_radius = bottom_radius
        self.top_radius = top_radius
        self.height = height
        self.num_points = 360
        super().__init__(**kwargs)

    def _build_vertices(self):
        h = self.height / 2.0
        
        bottom_vertices = [
            [0, -h, 0] # bottom center
        ]
        top_vertices = [
            [0, +h, 0] # top center
        ]
        
        for i in range(self.num_points + 1):
            angle = i * (2.0 * np.pi / self.num_points)
            bottom_x = self.bottom_radius * np.cos(angle)
            bottom_z = self.bottom_radius * np.sin(angle)
            top_x = self.top_radius * np.cos(angle)
            top_z = self.top_radius * np.sin(angle)
            
            bottom_vertice = [bottom_x, -h, bottom_z]
            top_vertice = [top_x, +h, top_z]
            bottom_vertices.append(bottom_vertice)
            top_vertices.append(top_vertice)
        
        side_vertices = []
        
        for i in range(self.num_points):
            angle1 = i * (2.0 * np.pi / self.num_points)
            bottom_x1 = self.bottom_radius * np.cos(angle1)
            bottom_z1 = self.bottom_radius * np.sin(angle1)
            top_x1 = self.top_radius * np.cos(angle1)
            top_z1 = self.top_radius * np.sin(angle1)
            
            angle2 = (i + 1) * (2.0 * np.pi / self.num_points)
            bottom_x2 = self.bottom_radius * np.cos(angle2)
            bottom_z2 = self.bottom_radius * np.sin(angle2)
            top_x2 = self.top_radius * np.cos(angle2)
            top_z2 = self.top_radius * np.sin(angle2)
            
            bottom_1 = [bottom_x1, -h, bottom_z1]
            top_1 = [top_x1, +h, top_z1]
            bottom_2 = [bottom_x2, -h, bottom_z2]
            top_2 = [top_x2, +h, top_z2]
            
            side_vertices.extend([top_1, bottom_2, bottom_1])
            side_vertices.extend([top_1, top_2, bottom_2])
        
        self.bottom_count = len(bottom_vertices)
        self.top_count = len(top_vertices)
        self.side_count = len(side_vertices)
        
        self.vertices = np.array(
            bottom_vertices + top_vertices + side_vertices,
            dtype=np.float32
        )
    
    def _build_normals(self):
        bottom_normals = np.tile([0.0, -1.0, 0.0], (self.bottom_count, 1))
        
        top_normals = np.tile([0.0, 1.0, 0.0], (self.top_count, 1))
        
        side_normals = []
        
        h = self.height
        dr = self.bottom_radius - self.top_radius
        len_n = np.sqrt(h**2 + dr**2)
        
        ny = dr / len_n
        nx_factor = h / len_n
        
        for i in range(self.num_points):
            angle1 = i * (2.0 * np.pi / self.num_points)
            n1 = [nx_factor * np.cos(angle1), ny, nx_factor * np.sin(angle1)]
            
            angle2 = (i + 1) * (2.0 * np.pi / self.num_points)
            n2 = [nx_factor * np.cos(angle2), ny, nx_factor * np.sin(angle2)]
            
            side_normals.extend([n1, n2, n1]) # [top_1, bottom_2, bottom_1]
            side_normals.extend([n1, n2, n2]) # [top_1, top_2, bottom_2]
            
        self.normals = np.vstack((bottom_normals, top_normals, side_normals)).astype(np.float32)
        
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
            top_colors = [
                [1.0, 1.0, 1.0] # top center
            ]
            
            for i in range(self.num_points + 1):
                angle = i * (2.0 * np.pi / self.num_points)
                
                r = np.cos(angle)
                g = np.sin(angle)
                b = 0.5 + 0.5 * np.cos(angle)
                
                bottom_colors.append([r, g, b])
                top_colors.append([r, g, b])
                
            side_colors = []
            
            for i in range(self.num_points):
                angle1 = i * (2.0 * np.pi / self.num_points)
                r1 = np.cos(angle1)
                g1 = np.sin(angle1)
                b1 = 0.5 + 0.5 * np.cos(angle1)
                color1 = [r1, g1, b1]
                
                angle2 = (i + 1) * (2.0 * np.pi / self.num_points)
                r2 = np.cos(angle2)
                g2 = np.sin(angle2)
                b2 = 0.5 + 0.5 * np.cos(angle2)
                color2 = [r2, g2, b2]
                
                side_colors.extend([color1, color2, color1])
                side_colors.extend([color1, color2, color1])
                
            self.colors = np.array(
                bottom_colors + top_colors + side_colors,
                dtype=np.float32
            )
        
    def _draw_model(self):
        offset = 0
        
        # bottom
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, offset, self.bottom_count)
        offset += self.bottom_count
        
        # top
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, offset, self.top_count)
        offset += self.top_count
        
        # side
        GL.glDrawArrays(GL.GL_TRIANGLES, offset, self.side_count)