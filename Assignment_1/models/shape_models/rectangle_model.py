import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class RectangleModel(BaseModel):
    def __init__(self, width, height, **kwargs):
        self.width = width
        self.height = height
        super().__init__(**kwargs)

    def _build_vertices(self):
        w, h = self.width / 2.0, self.height / 2.0
        
        self.vertices = np.array([
            [-w, -h, 0.0], # bottom left
            [+w, -h, 0.0], # bottom right
            [-w, +h, 0.0], # top left
            [+w, +h, 0.0], # top right
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
                [0.0, 1.0, 1.0],
            ], dtype=np.float32)
            
    def _build_texcoords(self):
        if self.render_mode == "Texture":
            self.texcoords = np.array([
                [0.0, 0.0],
                [1.0, 0.0],
                [0.0, 1.0],
                [1.0, 1.0],
            ], dtype=np.float32)
        
    def _draw_model(self):
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)