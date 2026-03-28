import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class PentagonModel(BaseModel):
    def __init__(self, vert_shader, frag_shader, radius, color):
        self.radius = radius
        self.num_points = 5
        self.color = color
        super().__init__(vert_shader, frag_shader)
        
    def _build_vertices(self):
        vertices = [
            [0, 0, 0] # center
        ]
        
        offset = np.pi / 2.0
        
        for i in range(self.num_points):
            angle = i * (2.0 * np.pi / self.num_points) + offset
            x = self.radius * np.cos(angle)
            y = self.radius * np.sin(angle)
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
        if 'flat' in self.vert_shader.lower():
            self.colors = np.tile(self.color, (len(self.vertices), 1)).astype(np.float32)
        else:
            colors = [
                [1.0, 1.0, 1.0] # center
            ]
            
            for i in range(self.num_points):
                angle = i * (2.0 * np.pi / self.num_points)
                
                r = np.cos(angle)
                g = np.sin(angle)
                b = 0.5 + 0.5 * np.cos(angle)
                
                colors.append([r, g, b])
                
            self.colors = np.array(
                colors,
                dtype=np.float32
            )
        
    def _draw_model(self):
        GL.glDrawElements(GL.GL_TRIANGLE_FAN, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)