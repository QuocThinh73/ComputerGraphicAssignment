import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class ArrowModel(BaseModel):
    def __init__(self, shaft_width, shaft_length, head_width, head_length, **kwargs):
        self.shaft_width = shaft_width
        self.shaft_length = shaft_length
        self.head_width = head_width
        self.head_length = head_length
        super().__init__(**kwargs)

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
                [1.0, 0.5, 0.0],
                [1.0, 0.8, 0.0],
                [1.0, 0.5, 0.0],
                [1.0, 0.8, 0.0],
                [1.0, 0.0, 0.0],
                [1.0, 0.0, 0.5],
                [1.0, 0.0, 0.0],
            ], dtype=np.float32)

    def _build_texcoords(self):
        if self.render_mode == "Texture":
            uvs = []
            
            total_length = self.shaft_length + self.head_length
            x_left = -total_length / 2.0
            
            max_half_width = max(self.shaft_width, self.head_width) / 2.0
            
            for v in self.vertices:
                u = (v[0] - x_left) / total_length
                
                if max_half_width == 0:
                    v_coord = 0.5
                else:
                    v_coord = 0.5 + (v[1] / (2.0 * max_half_width))
                    
                uvs.append([u, v_coord])
                
            self.texcoords = np.array(uvs, dtype=np.float32)
        
    def _draw_model(self):
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)