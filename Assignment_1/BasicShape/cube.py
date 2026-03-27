import numpy as np
import OpenGL.GL as GL

from libs.shader import *
from libs.buffer import *
from libs.lighting import LightingManager


class Cube(object):
    def __init__(self, vert_shader, frag_shader, width, height, depth):
        self.vert_shader = vert_shader
        self.frag_shader = frag_shader
        
        self.width = width
        self.height = height
        self.depth = depth

        self.vertices = self._build_vertices(self.width, self.height, self.depth)

        self.indices = np.array(
            [0, 4, 1, 5, 2, 6, 3, 7, 0, 4, 4, 0, 0, 3, 1, 2, 2, 4, 4, 7, 5, 6],
            dtype=np.int32
        )

        self.normals = self.vertices.copy()
        self.normals = self.normals / np.linalg.norm(self.normals, axis=1, keepdims=True)

        # colors: RGB format
        self.colors = np.array(
            [  # R    G    B
                [1.0, 0.0, 0.0],  # A <= Bottom: ABCD
                [1.0, 0.0, 1.0],  # B
                [0.0, 0.0, 1.0],  # C
                [0.0, 0.0, 0.0],  # D
                [1.0, 1.0, 0.0],  # E <= Top: EFGH
                [1.0, 1.0, 1.0],  # F
                [0.0, 1.0, 1.0],  # G
                [0.0, 1.0, 0.0],  # H
            ],
            dtype=np.float32
        )

        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        self.lighting = LightingManager(self.uma)
        
    def _build_vertices(self, width, height, depth):
        w = width / 2.0
        h = height / 2.0
        d = depth / 2.0
        
        return np.array([
            [-w, -h, +d],  # A
            [+w, -h, +d],  # B
            [+w, -h, -d],  # C
            [-w, -h, -d],  # D
            [-w, +h, +d],  # E
            [+w, +h, +d],  # F
            [+w, +h, -d],  # G
            [-w, +h, -d],  # H
        ], dtype=np.float32)

    """
    Create object -> call setup -> call draw
    """
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
        
        # Setup lighting if using Gouraud or Phong shader
        if 'gouraud' in self.vert_shader.lower():
            self.lighting.setup_gouraud()
        elif 'phong' in self.vert_shader.lower():
            self.lighting.setup_phong(mode=1)

        self.vao.activate()
        GL.glDrawElements(GL.GL_TRIANGLE_STRIP, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)
