import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class RectangleModel(BaseModel):
    def __init__(self, vert_shader, frag_shader, width, height, color):
        self.width = width
        self.height = height
        self.color = color
        super().__init__(vert_shader, frag_shader)
        
    def _build_vertices(self):
        w, h = self.width / 2.0, self.height / 2.0
        self.vertices = np.array([
            [-w, -h, 0.0],
            [+w, -h, 0.0],
            [-w, +h, 0.0],
            [+w, +h, 0.0],
        ], dtype=np.float32)

    def _build_indices(self):
        self.indices = np.array(
            [
                0, 2, 1, 
                2, 3, 1
            ], 
            dtype=np.int32
        )

    def _build_colors(self):
        if 'flat' in self.vert_shader.lower():
            self.colors = np.tile(self.color, (len(self.vertices), 1)).astype(np.float32)
        else:
            self.colors = np.array([
                [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], 
                [0.0, 0.0, 1.0], [0.0, 1.0, 1.0]
            ], dtype=np.float32)
        
    def _draw_model(self):
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)