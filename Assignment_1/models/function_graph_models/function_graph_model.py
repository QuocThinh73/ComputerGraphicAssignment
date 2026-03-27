import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class FunctionGraphModel(BaseModel):
    def __init__(self, vert_shader, frag_shader, min_x, max_x, min_y, max_y, delta_x, delta_y):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.delta_x = delta_x
        self.delta_y = delta_y
        super().__init__(vert_shader, frag_shader)

    def _build_vertices(self):
        x_vals = np.arange(self.min_x, self.max_x + self.delta_x, self.delta_x)
        y_vals = np.arange(self.min_y, self.max_y + self.delta_y, self.delta_y)
        
        self.num_x = len(x_vals)
        self.num_y = len(y_vals)

        X, Y = np.meshgrid(x_vals, y_vals, indexing='ij')
        Z = np.sin(X) + np.cos(Y)

        self.Z_vals = Z
        
        self.vertices = np.stack([X.ravel(), Y.ravel(), Z.ravel()], axis=1).astype(np.float32)

    def _build_indices(self):
        indices = []
        for i in range(self.num_x - 1):
            for j in range(self.num_y - 1):
                top_left = i * self.num_y + j
                top_right = top_left + 1
                bottom_left = (i + 1) * self.num_y + j
                bottom_right = bottom_left + 1
                
                indices.extend([top_left, top_right, bottom_left])
                indices.extend([top_right, bottom_right, bottom_left])
                
        self.indices = np.array(indices, dtype=np.uint32)

    def _build_colors(self):
        Z_flat = self.Z_vals.ravel()
        z_min, z_max = np.min(Z_flat), np.max(Z_flat)
        
        if z_min == z_max:
            Z_norm = np.zeros_like(Z_flat)
        else:
            Z_norm = (Z_flat - z_min) / (z_max - z_min)
            
        colors = np.zeros((len(self.vertices), 3), dtype=np.float32)
        
        colors[:, 0] = Z_norm
        colors[:, 1] = np.sin(Z_norm * np.pi)
        colors[:, 2] = 1.0 - Z_norm
        
        self.colors = colors

    def _draw_model(self):
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)