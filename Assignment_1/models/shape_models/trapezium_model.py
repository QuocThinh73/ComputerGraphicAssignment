import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class TrapeziumModel(BaseModel):
    def __init__(self, bottom_width, top_width, height, **kwargs):
        self.bottom_width = bottom_width
        self.top_width = top_width
        self.height = height
        super().__init__(**kwargs)

    def _build_vertices(self):
        bw, tw, h = self.bottom_width / 2.0, self.top_width / 2.0, self.height / 2.0
        self.vertices = np.array([
            [-bw, -h, 0.0],
            [+bw, -h, 0.0],
            [-tw, +h, 0.0],
            [+tw, +h, 0.0],
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
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [1.0, 1.0, 0.0]
            ], dtype=np.float32)
        
    def _draw_model(self):
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)