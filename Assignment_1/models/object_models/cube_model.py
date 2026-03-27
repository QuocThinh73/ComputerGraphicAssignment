import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class CubeModel(BaseModel):
    def __init__(self, vert_shader, frag_shader, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        super().__init__(vert_shader, frag_shader)
        
    def _build_vertices(self):
        w, h, d = self.width / 2.0, self.height / 2.0, self.depth / 2.0
        self.vertices = np.array([
            [-w, -h, +d],  # A
            [+w, -h, +d],  # B
            [+w, -h, -d],  # C
            [-w, -h, -d],  # D
            [-w, +h, +d],  # E
            [+w, +h, +d],  # F
            [+w, +h, -d],  # G
            [-w, +h, -d],  # H
        ], dtype=np.float32)

    def _build_indices(self):
        self.indices = np.array(
            [0, 4, 1, 5, 2, 6, 3, 7, 0, 4, 4, 0, 0, 3, 1, 2, 2, 4, 4, 7, 5, 6],
            dtype=np.int32
        )

    def _build_colors(self):
        self.colors = np.array([
            [1.0, 0.0, 0.0], [1.0, 0.0, 1.0], [0.0, 0.0, 1.0], [0.0, 0.0, 0.0],
            [1.0, 1.0, 0.0], [1.0, 1.0, 1.0], [0.0, 1.0, 1.0], [0.0, 1.0, 0.0],
        ], dtype=np.float32)
        
    def _draw_model(self):
        GL.glDrawElements(GL.GL_TRIANGLE_STRIP, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)