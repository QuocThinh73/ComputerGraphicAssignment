import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel

class CircleModel(BaseModel):
    def __init__(self, vert_shader, frag_shader, radius):
        self.radius = radius
        self.num_points = 360
        super().__init__(vert_shader, frag_shader)
        
    def _build_vertices(self):
        vertices = [
            [0, 0, 0] # center
        ]  
        
        for i in range(self.num_points):
            angle_deg = 90 + i * (360 / self.num_points)
            angle_rad = np.radians(angle_deg)
            x = self.radius * np.cos(angle_rad)
            y = self.radius * np.sin(angle_rad)
            vertices.append([x, y, 0])
        
        self.vertices = np.array(
            vertices, 
            dtype=np.float32
        )
        
    def _build_indices(self):
        indices = [0]
        indices.extend(range(1, self.num_points + 1))
        indices.append(1)
        
        self.indices = np.array(
            indices, 
            dtype=np.uint32
        )

    def _build_colors(self):
        colors = [
            [1.0, 1.0, 1.0] # center
        ]
        
        for i in range(self.num_points):
            angle_deg = 90 + i * (360 / self.num_points)
            angle_rad = np.radians(angle_deg)
            
            r = 0.5 + 0.5 * np.cos(angle_rad)
            g = 0.5 + 0.5 * np.sin(angle_rad)
            b = 0.5 + 0.5 * np.cos(angle_rad + 2.094)
            
            colors.append([r, g, b])
            
        self.colors = np.array(
            colors,
            dtype=np.float32
        )
        
    def _draw_model(self):
        GL.glDrawElements(GL.GL_TRIANGLE_FAN, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)