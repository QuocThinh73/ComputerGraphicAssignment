import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class PrismModel(BaseModel):
    def __init__(self, radius, height, num_sides, **kwargs):
        self.radius = radius
        self.height = height
        self.num_sides = num_sides
        super().__init__(**kwargs)
        
    def _build_vertices(self):
        h, r = self.height / 2.0, self.radius
        
        bottom_vertices = [[0, -h, 0]] # bottom center
        top_vertices = [[0, +h, 0]]    # top center
        side_vertices = []
        
        for i in range(self.num_sides + 1):
            angle = i * (2.0 * np.pi / self.num_sides)
            x = r * np.cos(angle)
            z = r * np.sin(angle)
            
            bottom_vertices.append([x, -h, z])
            top_vertices.append([x, +h, z])

        for i in range(self.num_sides):
            angle1 = i * (2.0 * np.pi / self.num_sides)
            angle2 = (i + 1) * (2.0 * np.pi / self.num_sides)
            
            x1, z1 = r * np.cos(angle1), r * np.sin(angle1)
            x2, z2 = r * np.cos(angle2), r * np.sin(angle2)
            
            b1 = [x1, -h, z1]
            t1 = [x1, +h, z1]
            b2 = [x2, -h, z2]
            t2 = [x2, +h, z2]
            
            side_vertices.extend([b1, t1, b2])
            side_vertices.extend([b2, t1, t2])
            
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
        
        for i in range(self.num_sides):
            angle1 = i * (2.0 * np.pi / self.num_sides)
            angle2 = (i + 1) * (2.0 * np.pi / self.num_sides)
            
            mid_angle = (angle1 + angle2) / 2.0
            nx = np.cos(mid_angle)
            nz = np.sin(mid_angle)
            face_normal = [nx, 0.0, nz]
            
            side_normals.extend([face_normal] * 6)
            
        self.normals = np.vstack((bottom_normals, top_normals, side_normals)).astype(np.float32)

    def _build_colors(self):
        shader_name = self.vert_shader.lower()
        if 'gouraud' in shader_name or 'phong' in shader_name:
            self.colors = np.zeros_like(self.vertices, dtype=np.float32)
        elif 'flat' in shader_name:
            self.colors = np.tile(self.color, (len(self.vertices), 1)).astype(np.float32)
        else:
            bottom_colors = [[1.0, 1.0, 1.0]]
            top_colors = [[1.0, 1.0, 1.0]]
            side_colors = []
            
            for i in range(self.num_sides + 1):
                angle = i * (2.0 * np.pi / self.num_sides)
                c = [np.cos(angle), np.sin(angle), 0.5 + 0.5 * np.cos(angle)]
                bottom_colors.append(c)
                top_colors.append(c)
                
            for i in range(self.num_sides):
                angle = i * (2.0 * np.pi / self.num_sides)
                r = 0.5 + 0.5 * np.cos(angle)
                g = 0.5 + 0.5 * np.sin(angle * 2)
                b = 0.5 + 0.5 * np.cos(angle + 1)
                face_color = [r, g, b]
                
                side_colors.extend([face_color] * 6)
                
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