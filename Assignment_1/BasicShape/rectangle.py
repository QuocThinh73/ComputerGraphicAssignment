import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np

from libs.shader import *
from libs.buffer import *
from libs.lighting import LightingManager
from libs import transform as T


class Rectangle:
    def __init__(self, vert_shader, frag_shader, width, height):
        self.vert_shader = vert_shader
        self.frag_shader = frag_shader
        
        self.width = width
        self.height = height
        
        self.vertices = self._build_vertices(self.width, self.height)
        
        self.indices = np.array(
            [0, 1, 2, 3],
            dtype=np.int32
        )
        
        normals = np.random.normal(0, 3, (3, 3)).astype(np.float32)
        normals[:, 2] = np.abs(normals[:, 2])
        self.normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)

        # colors: RGB format
        self.colors = np.array([
            [1.0, 0.0, 0.0], # vertex A
            [0.0, 1.0, 0.0], # vertex B
            [0.0, 0.0, 1.0], # vertex C
            [0.0, 1.0, 1.0]  # vertex D
        ], dtype=np.float32)

        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        self.lighting = LightingManager(self.uma)
        
    def _build_vertices(self, width, height):
        w = width / 2.0
        h = height / 2.0
        
        return np.array([
            [-w, -h, 0.0],   # A
            [+w, -h, 0.0],   # B
            [-w, +h, 0.0],   # C
            [+w, +h, 0.0],   # D
        ], dtype=np.float32)

    def setup(self):
        # setup VAO for drawing cube
        self.vao.add_vbo(0, self.vertices, ncomponents=3, stride=0, offset=None)
        self.vao.add_vbo(1, self.colors, ncomponents=3, stride=0, offset=None)
        
        # Add normals for Gouraud/Phong shading (if shader needs it)
        if 'gouraud' in self.vert_shader.lower() or 'phong' in self.vert_shader.lower():
            self.vao.add_vbo(2, self.normals, ncomponents=3, stride=0, offset=None)

        # setup EBO
        self.vao.add_ebo(self.indices)

        return self

    def draw(self, projection, view, model):
        GL.glUseProgram(self.shader.render_idx)
        modelview = view

        self.uma.upload_uniform_matrix4fv(projection, 'projection', True)
        self.uma.upload_uniform_matrix4fv(modelview, 'modelview', True)
        
        self.vao.activate()
        
        GL.glDrawElements(GL.GL_TRIANGLE_STRIP, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)
        self.vao.deactivate()