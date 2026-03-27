import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class ArrowModel(BaseModel):
    def __init__(self, vert_shader, frag_shader, shaft_width, shaft_length, head_width, head_length):
        self.shaft_width = shaft_width
        self.shaft_length = shaft_length
        self.head_width = head_width
        self.head_length = head_length
        super().__init__(vert_shader, frag_shader)
        
    def _build_vertices(self):
        total_length = self.shaft_length + self.head_length
        
        x_left = -total_length / 2.0
        x_mid = x_left + self.shaft_length
        x_right = total_length / 2.0
        
        sw = self.shaft_width / 2.0
        hw = self.head_width / 2.0
        
        self.vertices = np.array([
            # shaft
            [x_left, -sw, 0.0],
            [x_mid, -sw, 0.0],
            [x_left, +sw, 0.0],
            [x_mid, +sw, 0.0],
            
            # head
            [x_mid, -hw, 0.0],
            [x_right, 0.0, 0.0],
            [x_mid, +hw, 0.0],
        ], dtype=np.float32)

    def _build_indices(self):
        self.indices = np.array([
            0, 1, 2,
            1, 3, 2,
            4, 5, 6
        ], dtype=np.uint32)

    def _build_colors(self):
        self.colors = np.array([
            [1.0, 0.5, 0.0],
            [1.0, 0.8, 0.0],
            [1.0, 0.5, 0.0],
            [1.0, 0.8, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 0.0, 0.5],
            [1.0, 0.0, 0.0],
        ], dtype=np.float32)
        
    def _draw_model(self):
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)