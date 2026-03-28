import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class TorusModel(BaseModel):
    def __init__(self, vert_shader, frag_shader, major_radius, minor_radius, color):
        self.major_radius = major_radius
        self.minor_radius = minor_radius
        
        self.major_segments = 360
        self.minor_segments = 360
        
        self.color = color
        
        super().__init__(vert_shader, frag_shader)

    def _build_vertices(self):
        vertices = []
        
        for i in range(self.major_segments + 1):
            theta = i * (2.0 * np.pi / self.major_segments)
            cos_theta = np.cos(theta)
            sin_theta = np.sin(theta)
            
            for j in range(self.minor_segments + 1):
                phi = j * (2.0 * np.pi / self.minor_segments)
                cos_phi = np.cos(phi)
                sin_phi = np.sin(phi)
                
                x = (self.major_radius + self.minor_radius * cos_phi) * cos_theta
                y = (self.major_radius + self.minor_radius * cos_phi) * sin_theta
                z = self.minor_radius * sin_phi
                
                vertices.append([x, y, z])
                
        self.vertices = np.array(vertices, dtype=np.float32)

    def _build_indices(self):
        indices = []
        
        for i in range(self.major_segments):
            for j in range(self.minor_segments):
                next_i = i + 1
                next_j = j + 1
                
                v0 = i * (self.minor_segments + 1) + j
                v1 = next_i * (self.minor_segments + 1) + j
                v2 = next_i * (self.minor_segments + 1) + next_j
                v3 = i * (self.minor_segments + 1) + next_j
                
                indices.extend([v0, v1, v2, v0, v2, v3])
                
        self.indices = np.array(indices, dtype=np.uint32)
        
    def _build_normals(self):
        normals = []
        
        for i in range(self.major_segments + 1):
            theta = i * (2.0 * np.pi / self.major_segments)
            cos_theta = np.cos(theta)
            sin_theta = np.sin(theta)
            
            for j in range(self.minor_segments + 1):
                phi = j * (2.0 * np.pi / self.minor_segments)
                cos_phi = np.cos(phi)
                sin_phi = np.sin(phi)
                
                nx = cos_phi * cos_theta
                ny = cos_phi * sin_theta
                nz = sin_phi
                
                normals.append([nx, ny, nz])
                
        self.normals = np.array(normals, dtype=np.float32)

    def _build_colors(self):
        shader_name = self.vert_shader.lower()
        if 'gouraud' in shader_name or 'phong' in shader_name:
            self.colors = np.zeros_like(self.vertices, dtype=np.float32)
        elif 'flat' in shader_name:
            self.colors = np.tile(self.color, (len(self.vertices), 1)).astype(np.float32)
        else:
            colors = []
            
            for i in range(self.major_segments + 1):
                theta = i * (2.0 * np.pi / self.major_segments)
                
                for j in range(self.minor_segments + 1):
                    phi = j * (2.0 * np.pi / self.minor_segments)
                    
                    r = 0.5 + 0.5 * np.cos(theta)
                    g = 0.5 + 0.5 * np.sin(theta + phi)
                    b = 0.5 + 0.5 * np.cos(phi)
                    
                    colors.append([r, g, b])
                    
            self.colors = np.array(colors, dtype=np.float32)

    def _draw_model(self):
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)