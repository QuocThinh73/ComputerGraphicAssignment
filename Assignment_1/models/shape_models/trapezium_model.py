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
            [-bw, -h, 0.0], # bottom left
            [+bw, -h, 0.0], # bottom right
            [-tw, +h, 0.0], # top left
            [+tw, +h, 0.0], # top right
        ], dtype=np.float32)

    def _build_indices(self):
        self.indices = np.array(
            [
                0, 2, 1, 
                2, 3, 1
            ], 
            dtype=np.int32
        )

    def _build_normals(self):
        self.normals = np.tile([0.0, 0.0, 1.0], (len(self.vertices), 1)).astype(np.float32)

    def _build_colors(self):
        if self.render_mode in ["Gouraud", "Phong"]:
            self.colors = np.zeros_like(self.vertices, dtype=np.float32)
            
        elif self.render_mode == "Flat":
            flat_color = getattr(self, 'color', (1.0, 1.0, 1.0))
            self.colors = np.tile(flat_color, (len(self.vertices), 1)).astype(np.float32)
            
        elif self.render_mode == "Texture":
            self.colors = np.ones_like(self.vertices, dtype=np.float32)
            
        else:
            self.colors = np.array([
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [1.0, 1.0, 0.0],
            ], dtype=np.float32)

    def _build_texcoords(self):
        if self.render_mode == "Texture":
            max_w = max(self.bottom_width, self.top_width) / 2.0
            bw, tw = self.bottom_width / 2.0, self.top_width / 2.0
            
            u_b_left  = 0.5 - 0.5 * (bw / max_w)
            u_b_right = 0.5 + 0.5 * (bw / max_w)
            u_t_left  = 0.5 - 0.5 * (tw / max_w)
            u_t_right = 0.5 + 0.5 * (tw / max_w)

            self.texcoords = np.array([
                [u_b_left,  0.0],
                [u_b_right, 0.0],
                [u_t_left,  1.0],
                [u_t_right, 1.0],
            ], dtype=np.float32)
        
    def _draw_model(self):
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)