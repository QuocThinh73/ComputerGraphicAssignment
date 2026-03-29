import OpenGL.GL as GL              
import numpy as np

from libs.shader import *
from libs.buffer import *
from libs.lighting import LightingManager, Material
from libs import transform as T

SHADER_FILES = {
    "Flat": ("shaders/flat.vert", "shaders/flat.frag"),
    "Texture": ("shaders/texture.vert", "shaders/texture.frag"),
    "Gouraud": ("shaders/gouraud.vert", "shaders/gouraud.frag"),
    "Phong": ("shaders/phong.vert", "shaders/phong.frag"),
    "ColorInterp": ("shaders/color_interp.vert", "shaders/color_interp.frag") 
}


class BaseModel:
    def __init__(self, render_mode="Flat", **kwargs):
        self.render_mode = render_mode
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
        if render_mode not in SHADER_FILES:
            raise ValueError(f"Render mode '{render_mode}' is not supported.")
            
        self.vert_shader, self.frag_shader = SHADER_FILES[render_mode]
        
        self.vertices = None
        self.indices = None
        self.normals = None
        self.colors = None
        self.texcoords = None
        
        self._build_vertices()
        self._build_indices()
        self._build_normals()
        self._build_colors()
        
        if self.render_mode == "Texture":
            self._build_texcoords()

        self.vao = VAO()
        self.shader = Shader(self.vert_shader, self.frag_shader)
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
        
        if self.render_mode == "Texture":
            self.umanager = UManager(self.shader)
            self.umanager.setup_texture("texture1", self.texture_path)

        return self

    def draw(self, projection, view, model, lights=None):
        GL.glUseProgram(self.shader.render_idx)
        modelview = view @ model

        self.uma.upload_uniform_matrix4fv(projection, 'projection', True)
        self.uma.upload_uniform_matrix4fv(modelview, 'modelview', True)
        
        if self.render_mode in ["Gouraud", "Phong"]:
            current_mat = Material(
                diffuse=self.diffuse,
                specular=self.specular,
                ambient=self.ambient,
                shininess=self.shininess
            )
            
            if self.render_mode == "Gouraud":
                self.lighting.setup_gouraud(lights=lights, material=current_mat, shininess=current_mat.shininess)
            elif self.render_mode == "Phong":
                self.lighting.setup_phong(lights=lights, material=current_mat, mode=1)
        
        self.vao.activate()
        
        self._draw_model()
        
        self.vao.deactivate()
        
    def _draw_model(self): raise NotImplementedError