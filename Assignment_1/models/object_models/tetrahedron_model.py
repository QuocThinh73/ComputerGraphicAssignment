import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class TetrahedronModel(BaseModel):
    def __init__(self, size, **kwargs):
        self.size = size
        super().__init__(**kwargs)

    def _build_vertices(self):
        s = self.size
        
        A = [0.0, s, 0.0]
        B = [0.0, -s / 3.0, s * np.sqrt(8.0/9.0)]
        C = [-s * np.sqrt(2.0/3.0), -s / 3.0, -s * np.sqrt(2.0/9.0)]
        D = [s * np.sqrt(2.0/3.0), -s / 3.0, -s * np.sqrt(2.0/9.0)]

        self.faces = [
            [A, B, D], # right
            [A, D, C], # behind
            [A, C, B], # left
            [B, C, D]  # bottom
        ]
        
        vertices = []
        for face in self.faces:
            vertices.extend(face)
            
        self.vertices = np.array(vertices, dtype=np.float32)
        
    def _build_normals(self):
        normals = []
        for face in self.faces:
            p1 = np.array(face[0])
            p2 = np.array(face[1])
            p3 = np.array(face[2])
            
            v = p2 - p1
            w = p3 - p1
            n = np.cross(v, w)
            n = n / np.linalg.norm(n)
            
            normals.extend([n, n, n])
            
        self.normals = np.array(normals, dtype=np.float32)

    def _build_colors(self):
        shader_name = self.vert_shader.lower()
        if 'gouraud' in shader_name or 'phong' in shader_name:
            self.colors = np.zeros_like(self.vertices, dtype=np.float32)
        elif 'flat' in shader_name:
            self.colors = np.tile(self.color, (len(self.vertices), 1)).astype(np.float32)
        else:
            c0 = [1.0, 0.0, 0.0]
            c1 = [0.0, 1.0, 0.0]
            c2 = [0.0, 0.0, 1.0]
            c3 = [1.0, 1.0, 0.0]
            
            colors = []
            colors.extend([c0, c0, c0])
            colors.extend([c1, c1, c1])
            colors.extend([c2, c2, c2])
            colors.extend([c3, c3, c3])
            
            self.colors = np.array(colors, dtype=np.float32)
        
    def _draw_model(self):
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self.vertices))