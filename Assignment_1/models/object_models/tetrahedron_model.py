import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class TetrahedronModel(BaseModel):
    def __init__(self, vert_shader, frag_shader, size):
        self.size = size
        super().__init__(vert_shader, frag_shader)
        
    def _build_vertices(self):
        s = self.size
        self.vertices = np.array([
            [+s, +s, +s],
            [+s, -s, -s],
            [-s, +s, -s],
            [-s, -s, +s],
        ], dtype=np.float32)

    def _build_indices(self):
        self.indices = np.array([
            0, 1, 2,
            0, 2, 3,
            0, 3, 1,
            1, 3, 2
        ], dtype=np.uint32)

    def _build_colors(self):
        self.colors = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [1.0, 1.0, 0.0],
        ], dtype=np.float32)
        
    def _draw_model(self):
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)