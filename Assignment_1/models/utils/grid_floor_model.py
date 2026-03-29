import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel

class GridFloorModel(BaseModel):
    def __init__(self, vert_shader, frag_shader, size, spacing, show_x, show_y, show_z):
        self.size = size
        self.spacing = spacing
        self.show_x = show_x
        self.show_y = show_y
        self.show_z = show_z
        
        super().__init__(vert_shader, frag_shader)

    def _build_vertices(self):
        minor_verts, major_verts, axis_verts = [], [], []
        
        self._minor_colors, self._major_colors, self._axis_colors = [], [], []

        c_minor = [0.3, 0.3, 0.3]
        c_major = [0.65, 0.65, 0.65]
        c_x_axis = [1.0, 0.1, 0.1]
        c_y_axis = [0.1, 1.0, 0.1]
        c_z_axis = [0.1, 0.1, 1.0]

        vals = np.arange(-self.size, self.size + self.spacing, self.spacing)

        def add_line(v1, v2, check_val):
            if check_val == 0:
                pass
            elif check_val % 10 == 0:
                major_verts.extend([v1, v2])
                self._major_colors.extend([c_major, c_major])
            else:
                minor_verts.extend([v1, v2])
                self._minor_colors.extend([c_minor, c_minor])

        # Oxz
        if self.show_x and self.show_z:
            for x in vals: add_line([x, 0.0, -self.size], [x, 0.0, self.size], int(round(x)))
            for z in vals: add_line([-self.size, 0.0, z], [self.size, 0.0, z], int(round(z)))

        # Oxy
        if self.show_x and self.show_y:
            for x in vals: add_line([x, -self.size, 0.0], [x, self.size, 0.0], int(round(x)))
            for y in vals: add_line([-self.size, y, 0.0], [self.size, y, 0.0], int(round(y)))

        # Oyz
        if self.show_y and self.show_z:
            for y in vals: add_line([0.0, y, -self.size], [0.0, y, self.size], int(round(y)))
            for z in vals: add_line([0.0, -self.size, z], [0.0, self.size, z], int(round(z)))

        # X-axis, Y-axis, Z-axis
        if self.show_x:
            axis_verts.extend([[-self.size, 0.0, 0.0], [self.size, 0.0, 0.0]])
            self._axis_colors.extend([c_x_axis, c_x_axis])
        if self.show_y:
            axis_verts.extend([[0.0, -self.size, 0.0], [0.0, self.size, 0.0]])
            self._axis_colors.extend([c_y_axis, c_y_axis])
        if self.show_z:
            axis_verts.extend([[0.0, 0.0, -self.size], [0.0, 0.0, self.size]])
            self._axis_colors.extend([c_z_axis, c_z_axis])

        self.minor_count = len(minor_verts)
        self.major_count = len(major_verts)
        self.axis_count = len(axis_verts)

        if not (minor_verts or major_verts or axis_verts):
            self.vertices = np.zeros((0, 3), dtype=np.float32)
        else:
            self.vertices = np.array(minor_verts + major_verts + axis_verts, dtype=np.float32)

    def _build_colors(self):
        if not hasattr(self, '_minor_colors') or not (self._minor_colors or self._major_colors or self._axis_colors):
            self.colors = np.zeros((0, 3), dtype=np.float32)
        else:
            self.colors = np.array(self._minor_colors + self._major_colors + self._axis_colors, dtype=np.float32)

    def _build_indices(self):
        self.indices = None

    def _build_normals(self):
        self.normals = np.zeros_like(self.vertices, dtype=np.float32)

    def _draw_model(self):
        if len(self.vertices) == 0:
            return
            
        offset = 0
        if self.minor_count > 0:
            GL.glDrawArrays(GL.GL_LINES, offset, self.minor_count)
            offset += self.minor_count
        if self.major_count > 0:
            GL.glDrawArrays(GL.GL_LINES, offset, self.major_count)
            offset += self.major_count
        if self.axis_count > 0:
            GL.glDrawArrays(GL.GL_LINES, offset, self.axis_count)