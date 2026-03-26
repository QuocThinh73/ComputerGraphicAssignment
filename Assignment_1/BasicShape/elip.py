import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np

from libs.shader import *
from libs.buffer import *
from libs.lighting import LightingManager
from libs import transform as T


class Elip:
    def __init__(self, vert_shader, frag_shader):
        self.vert_shader = vert_shader
        self.frag_shader = frag_shader
        
        num_points = 180
        a = 0.9
        b = 0.5
        vertices = [
            [0, 0, 0] # center
        ]  
        
        for i in range(num_points):
            angle_deg = 90 + i * (360 / num_points)
            angle_rad = np.radians(angle_deg)
            x = a * np.cos(angle_rad)
            y = b * np.sin(angle_rad)
            vertices.append([x, y, 0])
        vertices.append(vertices[1])
        
        self.vertices = np.array(
            vertices, 
            dtype=np.float32
        )
        
        normals = np.random.normal(0, 3, (len(self.vertices), 3)).astype(np.float32)
        normals[:, 2] = np.abs(normals[:, 2])
        self.normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)

        # colors: RGB format
        colors = [
            [1.0, 0.0, 0.0] # center
        ]
        
        for i in range(num_points):
            colors.append(np.random.rand(3))
        colors.append(colors[1])
        
        self.colors = np.array(
            colors,
            dtype=np.float32
        )

        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        self.lighting = LightingManager(self.uma)

    def setup(self):
        self.vao.add_vbo(0, # index of the attribute in shader
                         self.vertices, # variable in python program
                         ncomponents=3, # x,y,x
                         dtype=GL.GL_FLOAT, # type GL_FLOAT = float32 in numpy (careful)
                         normalized=False,  # normalize vector or not (when normal)
                         stride=0,
                         offset=None)
        self.vao.add_vbo(1, self.colors, ncomponents=3, dtype=GL.GL_FLOAT, normalized=False, stride=0, offset=None)
        self.vao.add_vbo(2, self.normals, ncomponents=3, dtype=GL.GL_FLOAT, normalized=False, stride=0, offset=None)

        GL.glUseProgram(self.shader.render_idx)
        projection = T.ortho(-1, 1, -1, 1, -1, 1)
        modelview = np.identity(4, 'f')
        self.uma.upload_uniform_matrix4fv(projection, 'projection', True)
        self.uma.upload_uniform_matrix4fv(modelview, 'modelview', True)

        # Detect shader type and setup lighting accordingly
        if 'gouraud' in self.vert_shader.lower():
            # Gouraud shading computes lighting in vertex shader
            self.lighting.setup_gouraud()
        elif 'phong' in self.vert_shader.lower():
            # Phong shading computes lighting in fragment shader
            self.lighting.setup_phong(mode=1)
            
        return self

    def draw(self, projection, view, model):
        GL.glUseProgram(self.shader.render_idx)
        
        self.vao.activate()
        
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 0, len(self.vertices))
        self.vao.deactivate()