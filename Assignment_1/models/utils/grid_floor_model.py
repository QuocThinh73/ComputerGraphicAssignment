import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel 

class GridFloorModel(BaseModel):
    def __init__(self, vert_shader, frag_shader, size=50.0, spacing=1.0):
        self.size = size
        self.spacing = spacing
        super().__init__(vert_shader, frag_shader)

    def _build_vertices(self):
        minor_verts = []
        major_verts = []
        axis_verts = []

        vals = np.arange(-self.size, self.size + self.spacing, self.spacing)

        for x in vals:
            v1 = [x, 0.0, -self.size]
            v2 = [x, 0.0, self.size]
            check_val = int(round(x)) 
            
            if check_val == 0:
                axis_verts.extend([v1, v2])
            elif check_val % 10 == 0:
                major_verts.extend([v1, v2])
            else:
                minor_verts.extend([v1, v2])

        for z in vals:
            v1 = [-self.size, 0.0, z]
            v2 = [self.size, 0.0, z]
            check_val = int(round(z))
            
            if check_val == 0:
                axis_verts.extend([v1, v2])
            elif check_val % 10 == 0:
                major_verts.extend([v1, v2])
            else:
                minor_verts.extend([v1, v2])

        self.minor_count = len(minor_verts)
        self.major_count = len(major_verts)
        self.axis_count = len(axis_verts)

        self.vertices = np.array(minor_verts + major_verts + axis_verts, dtype=np.float32)

    def _build_colors(self): 
        minor_colors = []
        major_colors = []
        axis_colors = []

        c_minor = [0.3, 0.3, 0.3]
        c_major = [0.65, 0.65, 0.65]
        c_x_axis = [1.0, 0.1, 0.1]
        c_z_axis = [0.1, 0.1, 1.0]

        vals = np.arange(-self.size, self.size + self.spacing, self.spacing)

        for x in vals:
            check_val = int(round(x)) 
            
            if check_val == 0:
                axis_colors.extend([c_z_axis, c_z_axis])
            elif check_val % 10 == 0:
                major_colors.extend([c_major, c_major])
            else:
                minor_colors.extend([c_minor, c_minor])

        for z in vals:
            check_val = int(round(z))
            
            if check_val == 0:
                axis_colors.extend([c_x_axis, c_x_axis])
            elif check_val % 10 == 0:
                major_colors.extend([c_major, c_major])
            else:
                minor_colors.extend([c_minor, c_minor])

        self.colors = np.array(minor_colors + major_colors + axis_colors, dtype=np.float32)

    def _draw_model(self):
        offset = 0

        if self.minor_count > 0:
            GL.glDrawArrays(GL.GL_LINES, offset, self.minor_count)
            offset += self.minor_count

        if self.major_count > 0:
            GL.glDrawArrays(GL.GL_LINES, offset, self.major_count)
            offset += self.major_count

        if self.axis_count > 0:
            GL.glDrawArrays(GL.GL_LINES, offset, self.axis_count)