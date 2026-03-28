import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class CubeModel(BaseModel):
    def __init__(self, vert_shader, frag_shader, width, height, depth, color):
        self.width = width
        self.height = height
        self.depth = depth
        self.color = color
        super().__init__(vert_shader, frag_shader)
        
    def _build_vertices(self):
        w, h, d = self.width / 2.0, self.height / 2.0, self.depth / 2.0
        
        A = [-w, -h, +d]
        B = [+w, -h, +d]
        C = [+w, -h, -d]
        D = [-w, -h, -d]
        E = [-w, +h, +d]
        F = [+w, +h, +d]
        G = [+w, +h, -d]
        H = [-w, +h, -d]

        self.vertices = np.array([
            A, B, F, E,  # front
            B, C, G, F,  # right
            C, D, H, G,  # back
            D, A, E, H,  # left
            E, F, G, H,  # top
            D, C, B, A   # bottom
        ], dtype=np.float32)

    def _build_indices(self):
        indices = []
        for i in range(6):
            offset = i * 4
            indices.extend([
                offset, offset + 1, offset + 2,
                offset, offset + 2, offset + 3
            ])
            
        self.indices = np.array(indices, dtype=np.uint32)
        
    def _build_normals(self):
        n_front  = [ 0.0,  0.0,  1.0]
        n_right  = [ 1.0,  0.0,  0.0]
        n_back   = [ 0.0,  0.0, -1.0]
        n_left   = [-1.0,  0.0,  0.0]
        n_top    = [ 0.0,  1.0,  0.0]
        n_bottom = [ 0.0, -1.0,  0.0]

        self.normals = np.array(
            [n_front]*4 + [n_right]*4 + [n_back]*4 + 
            [n_left]*4 + [n_top]*4 + [n_bottom]*4,
            dtype=np.float32
        )

    def _build_colors(self):
        shader_name = self.vert_shader.lower()
        if 'gouraud' in shader_name or 'phong' in shader_name:
            self.colors = np.zeros_like(self.vertices, dtype=np.float32)
        elif 'flat' in shader_name:
            self.colors = np.tile(self.color, (24, 1)).astype(np.float32)
        else:
            cA = [1.0, 0.0, 0.0]
            cB = [1.0, 0.0, 1.0]
            cC = [0.0, 0.0, 1.0]
            cD = [0.0, 0.0, 0.0]
            cE = [1.0, 1.0, 0.0]
            cF = [1.0, 1.0, 1.0]
            cG = [0.0, 1.0, 1.0]
            cH = [0.0, 1.0, 0.0]

            self.colors = np.array([
                cA, cB, cF, cE,  # front
                cB, cC, cG, cF,  # right
                cC, cD, cH, cG,  # back
                cD, cA, cE, cH,  # left
                cE, cF, cG, cH,  # top
                cD, cC, cB, cA   # bottom
            ], dtype=np.float32)
        
    def _draw_model(self):
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)