import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class Sphere1Model(BaseModel):
    def __init__(self, vert_shader, frag_shader, radius, sectors, stacks, color):
        self.radius = radius
        self.sectors = sectors # longitude
        self.stacks = stacks   # latitude
        self.color = color
        super().__init__(vert_shader, frag_shader)

    def _build_vertices(self):
        vertices = []
        
        for i in range(self.stacks):
            phi1 = np.pi * (-0.5 + float(i) / self.stacks)
            phi2 = np.pi * (-0.5 + float(i + 1) / self.stacks)
            
            for j in range(self.sectors):
                theta1 = 2.0 * np.pi * float(j) / self.sectors
                theta2 = 2.0 * np.pi * float(j + 1) / self.sectors
                
                def get_point(phi, theta):
                    x = self.radius * np.cos(phi) * np.cos(theta)
                    y = self.radius * np.sin(phi)
                    z = self.radius * np.cos(phi) * np.sin(theta)
                    return [x, y, z]
                
                p1 = get_point(phi1, theta1)
                p2 = get_point(phi1, theta2)
                p3 = get_point(phi2, theta1)
                p4 = get_point(phi2, theta2)
                
                vertices.extend([p1, p2, p3])
                vertices.extend([p2, p4, p3])
                
        self.vertices = np.array(vertices, dtype=np.float32)
        
    def _build_normals(self):
        self.normals = (self.vertices / self.radius).astype(np.float32)

    def _build_colors(self):
        shader_name = self.vert_shader.lower()
        if 'gouraud' in shader_name or 'phong' in shader_name:
            self.colors = np.zeros_like(self.vertices, dtype=np.float32)
        elif 'flat' in shader_name:
            self.colors = np.tile(self.color, (len(self.vertices), 1)).astype(np.float32)
        else:
            normalized_pos = self.vertices / self.radius
            self.colors = (normalized_pos + 1.0) / 2.0

    def _draw_model(self):
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self.vertices))
        
    
class Sphere2Model(BaseModel):
    def __init__(self, vert_shader, frag_shader, radius, segments, color):
        self.radius = radius
        self.segments = segments
        self.color = color
        super().__init__(vert_shader, frag_shader)

    def _build_vertices(self):
        vertices = []
        
        def build_face(u_axis, v_axis, w_axis, w_sign):
            for i in range(self.segments):
                for j in range(self.segments):
                    u1 = (i / self.segments) * 2.0 - 1.0
                    u2 = ((i + 1) / self.segments) * 2.0 - 1.0
                    v1 = (j / self.segments) * 2.0 - 1.0
                    v2 = ((j + 1) / self.segments) * 2.0 - 1.0
                    
                    def get_sphere_point(u, v):
                        point = np.zeros(3)
                        point[u_axis] = u
                        point[v_axis] = v
                        point[w_axis] = w_sign
                        point = (point / np.linalg.norm(point)) * self.radius
                        return point.tolist()
                    
                    p1 = get_sphere_point(u1, v1)
                    p2 = get_sphere_point(u2, v1)
                    p3 = get_sphere_point(u1, v2)
                    p4 = get_sphere_point(u2, v2)
                    
                    vertices.extend([p1, p2, p3])
                    vertices.extend([p2, p4, p3])

        build_face(0, 1, 2, 1.0)  # front (Z+)
        build_face(0, 1, 2, -1.0) # back (Z-)
        build_face(2, 1, 0, 1.0)  # right (X+)
        build_face(2, 1, 0, -1.0) # left (X-)
        build_face(0, 2, 1, 1.0)  # top (Y+)
        build_face(0, 2, 1, -1.0) # bottom (Y-)
        
        self.vertices = np.array(vertices, dtype=np.float32)
        
    def _build_normals(self):
        self.normals = (self.vertices / self.radius).astype(np.float32)

    def _build_colors(self):
        shader_name = self.vert_shader.lower()
        if 'gouraud' in shader_name or 'phong' in shader_name:
            self.colors = np.zeros_like(self.vertices, dtype=np.float32)
        elif 'flat' in shader_name:
            self.colors = np.tile(self.color, (len(self.vertices), 1)).astype(np.float32)
        else:
            normalized_pos = self.vertices / self.radius
            self.colors = (normalized_pos + 1.0) / 2.0

    def _draw_model(self):
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self.vertices))
        

class Sphere3Model(BaseModel):
    def __init__(self, vert_shader, frag_shader, radius, subdivisions, color):
        self.radius = radius
        self.subdivisions = subdivisions
        self.color = color
        super().__init__(vert_shader, frag_shader)

    def _build_vertices(self):
        A = np.array([1, 1, 1], dtype=np.float32)
        B = np.array([1, -1, -1], dtype=np.float32)
        C = np.array([-1, 1, -1], dtype=np.float32)
        D = np.array([-1, -1, 1], dtype=np.float32)

        triangles = [
            [A, B, C], [A, C, D], [A, D, B], [B, D, C]
        ]
        
        def get_mid_point(v1, v2):
            mid = (v1 + v2) / 2.0
            return (mid / np.linalg.norm(mid)) * self.radius

        for tri in triangles:
            for i in range(3):
                tri[i] = (tri[i] / np.linalg.norm(tri[i])) * self.radius

        for _ in range(self.subdivisions):
            new_triangles = []
            for tri in triangles:
                v0, v1, v2 = tri
                
                v01 = get_mid_point(v0, v1)
                v12 = get_mid_point(v1, v2)
                v20 = get_mid_point(v2, v0)
                
                new_triangles.extend([
                    [v0, v01, v20],
                    [v1, v12, v01],
                    [v2, v20, v12],
                    [v01, v12, v20]
                ])
            triangles = new_triangles

        vertices = []
        for tri in triangles:
            vertices.extend(tri)
            
        self.vertices = np.array(vertices, dtype=np.float32)
        
    def _build_normals(self):
        self.normals = (self.vertices / self.radius).astype(np.float32)

    def _build_colors(self):
        shader_name = self.vert_shader.lower()
        if 'gouraud' in shader_name or 'phong' in shader_name:
            self.colors = np.zeros_like(self.vertices, dtype=np.float32)
        elif 'flat' in shader_name:
            self.colors = np.tile(self.color, (len(self.vertices), 1)).astype(np.float32)
        else:
            normalized_pos = self.vertices / self.radius
            self.colors = (normalized_pos + 1.0) / 2.0

    def _draw_model(self):
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self.vertices))