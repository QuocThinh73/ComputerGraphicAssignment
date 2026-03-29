import numpy as np
from viewer.model_factory import build_shape
from models.utils.grid_floor_model import GridFloorModel
import OpenGL.GL as GL


def create_translation_matrix(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def create_rotation_matrix_x(deg):
    rad = np.radians(deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def create_rotation_matrix_y(deg):
    rad = np.radians(deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def create_rotation_matrix_z(deg):
    rad = np.radians(deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

class Scene:
    def __init__(self, state):
        self.state = state
        
        self.grid_model = GridFloorModel(
            render_mode="Flat",
            size=500.0, 
            spacing=1.0,
            show_x=self.state.show_grid_x,
            show_y=self.state.show_grid_y,
            show_z=self.state.show_grid_z
        ).setup()
        
        self.light_marker = build_shape(
            "Sphere1", 
            render_mode="Flat",
            radius=0.1,
            sectors=16,
            stacks=16,
            color=(1.0, 1.0, 0.5)
        )

    def update(self):
        if self.state.grid_need_rebuild:
            self.grid_model = GridFloorModel(
                render_mode="Flat",
                size=500.0, 
                spacing=1.0,
                show_x=self.state.show_grid_x,
                show_y=self.state.show_grid_y,
                show_z=self.state.show_grid_z
            ).setup()
            
            self.state.grid_need_rebuild = False
            
        for obj in self.state.scene_objects:
            if obj["need_rebuild"]:
                params = obj["state"].get_params_values()
                
                try:
                    obj["model"] = build_shape(obj["type"], **params)
                except Exception as e:
                    print(f"Error building {obj['type']}: {e}")
                    obj["model"] = None
                    
                obj["need_rebuild"] = False

    def draw(self, projection, view):
        if hasattr(self, 'grid_model') and self.grid_model is not None:
            model_matrix_grid = np.eye(4, dtype=np.float32)
            self.grid_model.draw(projection, view, model_matrix_grid)
            
        for obj in self.state.scene_objects:
            if obj["model"] is not None:
                tf = obj["state"].get_transform_values()
                
                T  = create_translation_matrix(tf['pos_x'], tf['pos_y'], tf['pos_z'])
                Rx = create_rotation_matrix_x(tf['rot_x'])
                Ry = create_rotation_matrix_y(tf['rot_y'])
                Rz = create_rotation_matrix_z(tf['rot_z'])
                
                model_matrix = T @ Ry @ Rx @ Rz
                
                if obj["state"].is_wireframe:
                    GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
                else:
                    GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
                
                obj["model"].draw(projection, view, model_matrix, lights=self.state.lights)
                
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
                
        for light in self.state.lights:
            if getattr(light, 'enabled', True):
                Lx, Ly, Lz = light.position
                T_light = create_translation_matrix(Lx, Ly, Lz)
                
                if hasattr(self, 'light_marker') and self.light_marker is not None:
                    self.light_marker.draw(projection, view, T_light)