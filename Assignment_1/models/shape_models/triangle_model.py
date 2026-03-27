import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class TriangleModel(BaseModel):
    def __init__(self, vert_shader, frag_shader, base, height):
        self.base = base
        self.height = height
        super().__init__(vert_shader, frag_shader)
        
    def _build_vertices(self):
        b, h = self.base / 2.0, self.height / 2.0
        self.vertices = np.array([
            [-b, -h, 0.0],
            [+b, -h, 0.0],
            [0.0, +h, 0.0],
        ], dtype=np.float32)

    def _build_indices(self):
        self.indices = np.array(
            [
                0, 2, 1
            ], 
            dtype=np.int32
        )

    def _build_colors(self):
        self.colors = np.array([
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ], dtype=np.float32)
        
    def _draw_model(self):
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)