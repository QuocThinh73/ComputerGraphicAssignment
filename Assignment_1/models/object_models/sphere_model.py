import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class Sphere1Model(BaseModel):
    def __init__(self, radius, sectors, stacks, **kwargs):
        self.radius = radius
        self.sectors = sectors # longitude
        self.stacks = stacks   # latitude
        super().__init__(**kwargs)

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
        if self.render_mode in ["Gouraud", "Phong"]:
            self.colors = np.zeros_like(self.vertices, dtype=np.float32)
            
        elif self.render_mode == "Flat":
            flat_color = getattr(self, 'color', (1.0, 1.0, 1.0))
            self.colors = np.tile(flat_color, (len(self.vertices), 1)).astype(np.float32)
            
        elif self.render_mode == "Texture":
            self.colors = np.ones_like(self.vertices, dtype=np.float32)
            
        else:
            normalized_pos = self.vertices / self.radius
            self.colors = (normalized_pos + 1.0) / 2.0

    def _build_texcoords(self):
        if self.render_mode == "Texture":
            uvs = []
            for i in range(self.stacks):
                v1 = float(i) / self.stacks
                v2 = float(i + 1) / self.stacks
                for j in range(self.sectors):
                    u1 = float(j) / self.sectors
                    u2 = float(j + 1) / self.sectors
                    
                    uv1, uv2, uv3, uv4 = [u1, v1], [u2, v1], [u1, v2], [u2, v2]
                    uvs.extend([uv1, uv2, uv3])
                    uvs.extend([uv2, uv4, uv3])
                    
            self.texcoords = np.array(uvs, dtype=np.float32)

    def _draw_model(self):
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self.vertices))
        
    
class Sphere2Model(BaseModel):
    def __init__(self, radius, segments, **kwargs):
        self.radius = radius
        self.segments = segments
        super().__init__(**kwargs)

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
        
    def _build_colors(self):
        if self.render_mode in ["Gouraud", "Phong"]:
            self.colors = np.zeros_like(self.vertices, dtype=np.float32)
            
        elif self.render_mode == "Flat":
            flat_color = getattr(self, 'color', (1.0, 1.0, 1.0))
            self.colors = np.tile(flat_color, (len(self.vertices), 1)).astype(np.float32)
            
        elif self.render_mode == "Texture":
            self.colors = np.ones_like(self.vertices, dtype=np.float32)

        else:
            normalized_pos = self.vertices / self.radius
            self.colors = (normalized_pos + 1.0) / 2.0

    def _build_texcoords(self):
        if self.render_mode == "Texture":
            uvs = []
            for v in self.vertices:
                nx, ny, nz = v[0] / self.radius, v[1] / self.radius, v[2] / self.radius
                u = 0.5 + np.arctan2(nx, nz) / (2.0 * np.pi)
                v_coord = 0.5 + np.arcsin(ny) / np.pi
                uvs.append([u, v_coord])
            self.texcoords = np.array(uvs, dtype=np.float32)

    def _draw_model(self):
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self.vertices))
        

class Sphere3Model(BaseModel):
    def __init__(self, radius, subdivisions, **kwargs):
        self.radius = radius
        self.subdivisions = subdivisions
        super().__init__(**kwargs)

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
        if self.render_mode in ["Gouraud", "Phong"]:
            self.colors = np.zeros_like(self.vertices, dtype=np.float32)
            
        elif self.render_mode == "Flat":
            flat_color = getattr(self, 'color', (1.0, 1.0, 1.0))
            self.colors = np.tile(flat_color, (len(self.vertices), 1)).astype(np.float32)
            
        elif self.render_mode == "Texture":
            self.colors = np.ones_like(self.vertices, dtype=np.float32)
            
        else:
            normalized_pos = self.vertices / self.radius
            self.colors = (normalized_pos + 1.0) / 2.0

    def _build_texcoords(self):
        if self.render_mode == "Texture":
            uvs = []
            for v in self.vertices:
                nx, ny, nz = v[0] / self.radius, v[1] / self.radius, v[2] / self.radius
                u = 0.5 + np.arctan2(nx, nz) / (2.0 * np.pi)
                v_coord = 0.5 + np.arcsin(ny) / np.pi
                uvs.append([u, v_coord])
            self.texcoords = np.array(uvs, dtype=np.float32)

    def _draw_model(self):
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self.vertices))