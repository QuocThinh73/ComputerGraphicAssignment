import numpy as np
import OpenGL.GL as GL

from libs.shader import *
from libs.buffer import *
from libs.lighting import LightingManager


class Prism(object):
    def __init__(self, vert_shader, frag_shader):
        self.vert_shader = vert_shader
        self.frag_shader = frag_shader
        
        self.vertices = np.array(
            [
                [-1, -1, +1],  # A <= Bottom: ABC
                [+1, -1, +1],  # B
                [+1, -1, -1],  # C
                [-1, +1, +1],  # D <= Top: DEF
                [+1, +1, +1],  # E
                [+1, +1, -1],  # F
            ],
            dtype=np.float32
        )

        self.indices = np.array(
            [
                # Bottom
                0, 2, 1,
                # Top
                3, 4, 5,
                # Side
                0, 1, 4,
                0, 4, 3,
                1, 2, 5,
                1, 5, 4,
                2, 0, 3,
                2, 3, 5
            ],
            dtype=np.int32
        )

        self.normals = self.vertices.copy()
        self.normals = self.normals / np.linalg.norm(self.normals, axis=1, keepdims=True)
        
        # colors: RGB format
        self.colors = np.array(
            [  # R    G    B
                [1.0, 0.0, 0.0],  # A <= Bottom: ABC
                [1.0, 0.0, 1.0],  # B
                [0.0, 0.0, 1.0],  # C
                [0.0, 0.0, 0.0],  # D <= Top: DEF
                [1.0, 1.0, 0.0],  # E 
                [1.0, 1.0, 1.0],  # F
            ],
            dtype=np.float32
        )

        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        self.lighting = LightingManager(self.uma)

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

        # setup EBO for drawing cube
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
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)
