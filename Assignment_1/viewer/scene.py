import numpy as np
from viewer.model_factory import build_shape


class Scene:
    def __init__(self, state):
        self.state = state

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
        for obj in self.state.scene_objects:
            if obj["model"] is not None:
                model_matrix = np.eye(4, dtype=np.float32) 
                
                obj["model"].draw(projection, view, model_matrix)