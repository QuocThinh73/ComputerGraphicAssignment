import numpy as np
from viewer.model_factory import build_shape, SHADER_FILES
from models.utils.grid_floor_model import GridFloorModel


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
        
        vert_flat, frag_flat = SHADER_FILES["Flat"]
        self.grid_model = GridFloorModel(vert_flat, frag_flat, size=500.0, spacing=1.0).setup()

    def update(self):
        for obj in self.state.scene_objects:
            if obj["need_rebuild"]:
                params = obj["state"].get_params_values()
                
                try:
                    obj["model"] = build_shape(
                        obj["type"],
                        self.state.current_shader_name,
                        **params
                    )
                except Exception as e:
                    print(f"Error building {obj['type']}: {e}")
                    obj["model"] = None
                    
                obj["need_rebuild"] = False

    def draw(self, projection, view):
        if self.grid_model is not None:
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
                
                obj["model"].draw(projection, view, model_matrix)