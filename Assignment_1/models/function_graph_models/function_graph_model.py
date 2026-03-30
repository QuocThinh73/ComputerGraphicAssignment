import numpy as np
import OpenGL.GL as GL
from ..base_model import BaseModel


class FunctionGraphModel(BaseModel):
    def __init__(self, func_str, min_x, max_x, min_y, max_y, delta_x, delta_y, **kwargs):
        self.func_str = func_str
        self.func = self._parse_function(self.func_str)
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.delta_x = delta_x
        self.delta_y = delta_y
        super().__init__(**kwargs)
        
    def _parse_function(self, func_str):
        if not func_str.strip():
            return lambda x, y: np.zeros_like(x)
            
        math_env = {
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "log": np.log, "sqrt": np.sqrt,
            "pi": np.pi, "e": np.e, "abs": np.abs,
        }
        
        try:
            lambda_str = f"lambda x, y: {func_str}"
            
            func = eval(lambda_str, {"__builtins__": None}, math_env)
            
            func(np.array([0.1]), np.array([0.1])) 
            return func
            
        except Exception as e:
            return lambda x, y: np.zeros_like(x)

    def _build_vertices(self):
        if not self.func_str.strip():
            self.vertices = np.array([], dtype=np.float32)
            self.Z_vals = np.array([])
            return
            
        x_vals = np.arange(self.min_x, self.max_x + self.delta_x, self.delta_x)
        y_vals = np.arange(self.min_y, self.max_y + self.delta_y, self.delta_y)
        
        self.num_x = len(x_vals)
        self.num_y = len(y_vals)

        x, y = np.meshgrid(x_vals, y_vals, indexing='ij')
        
        z = self.func(x, y)
        
        if np.isscalar(z):
            z = np.full_like(x, float(z))

        self.Z_vals = z
        self.vertices = np.stack([x.ravel(), y.ravel(), z.ravel()], axis=1).astype(np.float32)

    def _build_indices(self):
        if not hasattr(self, 'num_x') or not self.func_str.strip():
            self.indices = np.array([], dtype=np.uint32)
            return
        
        indices = []
        for i in range(self.num_x - 1):
            for j in range(self.num_y - 1):
                tl = i * self.num_y + j
                tr = tl + 1
                bl = (i + 1) * self.num_y + j
                br = bl + 1
                
                indices.extend([tl, tr, bl])
                indices.extend([tr, br, bl])
                
        self.indices = np.array(indices, dtype=np.uint32)

    def _build_normals(self):
        if not self.func_str.strip() or len(self.vertices) == 0:
            self.normals = np.array([], dtype=np.float32)
            return
        
        dz_dx, dz_dy = np.gradient(self.Z_vals, self.delta_x, self.delta_y)
        
        nx = -dz_dx.ravel()
        ny = -dz_dy.ravel()
        nz = np.ones_like(nx)
        
        normals = np.stack([nx, ny, nz], axis=1)
        lengths = np.linalg.norm(normals, axis=1, keepdims=True)
        
        self.normals = (normals / lengths).astype(np.float32)

    def _build_colors(self):
        if not self.func_str.strip() or len(self.vertices) == 0:
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
            z_vals = self.vertices[:, 2]
            z_min, z_max = np.min(z_vals), np.max(z_vals)
            
            if z_min == z_max:
                z_norm = np.zeros_like(z_vals)
            else:
                z_norm = (z_vals - z_min) / (z_max - z_min)
                
            colors = np.zeros_like(self.vertices, dtype=np.float32)
            
            colors[:, 0] = np.clip(3.0 * z_norm - 1.0, 0.0, 1.0)
            colors[:, 1] = np.clip(1.5 - np.abs(3.0 * z_norm - 1.5), 0.0, 1.0)
            colors[:, 2] = np.clip(2.0 - 3.0 * z_norm, 0.0, 1.0)
            
            self.colors = colors

    def _draw_model(self):
        if not hasattr(self, 'indices') or len(self.indices) == 0:
            return
        
        GL.glDrawElements(GL.GL_TRIANGLES, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)