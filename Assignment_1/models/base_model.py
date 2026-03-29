import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np

from libs.shader import *
from libs.buffer import *
from libs.lighting import LightingManager
from libs import transform as T


class BaseModel:
    def __init__(self, vert_shader, frag_shader):
        self.vert_shader = vert_shader
        self.frag_shader = frag_shader
        
        self._build_vertices()
        self._build_indices()
        self._build_normals()
        self._build_colors()
        self._build_texcoords()

        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        self.lighting = LightingManager(self.uma)
        
    def _build_vertices(self): 
        self.vertices = None

    def _build_indices(self): 
        self.indices = None

    def _build_normals(self):
        self.normals = None

    def _build_colors(self):
        self.colors = None
        
    def _build_texcoords(self):
        self.texcoords = None

    def setup(self):
        # setup VAO
        self.vao.add_vbo(0, self.vertices, ncomponents=3, stride=0, offset=None)
        self.vao.add_vbo(1, self.colors, ncomponents=3, stride=0, offset=None)
        
        if hasattr(self, 'normals') and self.normals is not None and len(self.normals) > 0:
            self.vao.add_vbo(2, self.normals, ncomponents=3, stride=0, offset=None)
            
        if hasattr(self, 'texcoords') and self.texcoords is not None and len(self.texcoords) > 0:
            self.vao.add_vbo(3, self.texcoords, ncomponents=2, dtype=GL.GL_FLOAT)

        # setup EBO
        if self.indices is not None:
            self.vao.add_ebo(self.indices)
            
        tex_path = getattr(self, 'texture_path', None)
        if tex_path and "texture" in self.vert_shader.lower() and tex_path.strip() != "":
            self.umanager = UManager(self.shader)
            self.umanager.setup_texture("texture1", tex_path)

        return self

    def draw(self, projection, view, model, lights=None):
        GL.glUseProgram(self.shader.render_idx)
        modelview = view @ model

        self.uma.upload_uniform_matrix4fv(projection, 'projection', True)
        self.uma.upload_uniform_matrix4fv(modelview, 'modelview', True)
        
        if 'gouraud' in self.vert_shader.lower():
            self.lighting.setup_gouraud(lights=lights)
        elif 'phong' in self.vert_shader.lower():
            self.lighting.setup_phong(lights=lights, mode=1)
        
        self.vao.activate()
        
        self._draw_model()
        
        self.vao.deactivate()
        
    def _draw_model(self): raise NotImplementedError