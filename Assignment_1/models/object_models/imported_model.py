import numpy as np
import OpenGL.GL as GL
import trimesh
import os
from ..base_model import BaseModel


class ImportedModel(BaseModel):
    def __init__(self, file_path, scale_factor, **kwargs):
        self.file_path = file_path
        self.scale_factor = scale_factor
        self.mesh = None
        self._load_mesh()
        super().__init__(**kwargs)

    def _load_mesh(self):
        if not self.file_path or not os.path.exists(self.file_path):
            print(f"Chưa tìm thấy file: {self.file_path}")
            return
            
        try:
            self.mesh = trimesh.load(self.file_path, force='mesh')
            print(f"Đã load thành công: {self.file_path}")
        except Exception as e:
            print(f"Lỗi khi load file 3D: {e}")
            self.mesh = None

    def _build_vertices(self):
        if self.mesh is None:
            self.vertices = np.array([], dtype=np.float32)
            return
        
        vertices = self.mesh.vertices.copy()
        
        center = vertices.mean(axis=0)
        vertices -= center
        
        max_extent = np.max(vertices.max(axis=0) - vertices.min(axis=0))
        if max_extent > 0:
            vertices = (vertices / max_extent) * self.scale_factor
            
        self.vertices = np.array(vertices, dtype=np.float32)

    def _build_indices(self):
        if self.mesh is None:
            self.indices = np.array([], dtype=np.uint32)
            return
        self.indices = np.array(self.mesh.faces.flatten(), dtype=np.uint32)

    def _build_normals(self):
        if self.mesh is None:
            self.normals = np.array([], dtype=np.float32)
            return
        self.normals = np.array(self.mesh.vertex_normals, dtype=np.float32)

    def _build_colors(self):
        if self.mesh is None or len(self.vertices) == 0:
            self.colors = np.array([], dtype=np.float32)
            return
            
        if self.render_mode in ["Gouraud", "Phong"]:
            self.colors = np.zeros_like(self.vertices, dtype=np.float32)
            
        elif self.render_mode == "Flat":
            flat_color = getattr(self, 'color', (1.0, 1.0, 1.0))
            self.colors = np.tile(flat_color, (len(self.vertices), 1)).astype(np.float32)
            
        elif self.render_mode == "Texture":
            self.colors = np.ones_like(self.vertices, dtype=np.float32)
            
        else:
            min_y, max_y = np.min(self.vertices[:, 1]), np.max(self.vertices[:, 1])
            range_y = max_y - min_y if max_y != min_y else 1.0
            norm_y = (self.vertices[:, 1] - min_y) / range_y
            
            colors = np.zeros_like(self.vertices, dtype=np.float32)
            colors[:, 0] = norm_y
            colors[:, 1] = 1.0 - norm_y
            colors[:, 2] = 0.5
            self.colors = colors

    def _build_texcoords(self):
        if self.mesh is None or len(self.vertices) == 0:
            self.texcoords = np.array([], dtype=np.float32)
            return
            
        if self.render_mode == "Texture":
            if hasattr(self.mesh.visual, 'uv') and self.mesh.visual.uv is not None and len(self.mesh.visual.uv) == len(self.vertices):
                self.texcoords = np.array(self.mesh.visual.uv, dtype=np.float32)
            else:
                vertices_norm = self.vertices / np.linalg.norm(self.vertices, axis=1, keepdims=True)
                u = 0.5 + np.arctan2(vertices_norm[:, 0], vertices_norm[:, 2]) / (2 * np.pi)
                v = 0.5 - np.arcsin(vertices_norm[:, 1]) / np.pi
                self.texcoords = np.column_stack((u, v)).astype(np.float32)

    def _draw_model(self):
        if self.mesh is None or len(self.indices) == 0:
            return
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)