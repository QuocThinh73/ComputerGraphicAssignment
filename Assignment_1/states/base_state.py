from configs import *

class Parameter:
    def __init__(self, label, value, min_val, max_val):
        self.label = label
        self.value = value
        self.min_val = min_val
        self.max_val = max_val

class FloatParam(Parameter):
    def __init__(self, label, value, min_val=0.1, max_val=10.0):
        super().__init__(label, float(value), float(min_val), float(max_val))

class IntParam(Parameter):
    def __init__(self, label, value, min_val=1, max_val=100):
        super().__init__(label, int(value), int(min_val), int(max_val))
        
class StringParam(Parameter):
    def __init__(self, label, value):
        super().__init__(label, str(value), None, None)
        
class ColorParam(Parameter):
    def __init__(self, label, value=(1.0, 1.0, 1.0)):
        super().__init__(label, value, None, None)

class BaseState:
    def __init__(self, name):
        self.name = name
        
        self.params = {}
        
        self.material_params = {
            "color": ColorParam("Color", DEFAULT_COLOR),
            "diffuse": ColorParam("Diffuse", DEFAULT_MAT_DIFFUSE),
            "specular": ColorParam("Specular", DEFAULT_MAT_SPECULAR),
            "ambient": ColorParam("Ambient", DEFAULT_MAT_AMBIENT),
            "shininess": FloatParam("Shininess", DEFAULT_MAT_SHININESS, 1.0, 128.0),
            "texture_path": StringParam("Texture Path", ""),
        }
        
        self.transform_params = {
            "pos_x": FloatParam("Position X", 0.0, -20.0, 20.0),
            "pos_y": FloatParam("Position Y", 0.0, -20.0, 20.0),
            "pos_z": FloatParam("Position Z", 0.0, -20.0, 20.0),
            "rot_x": FloatParam("Rotation X", 0.0, -180.0, 180.0),
            "rot_y": FloatParam("Rotation Y", 0.0, -180.0, 180.0),
            "rot_z": FloatParam("Rotation Z", 0.0, -180.0, 180.0),
        }
        
        self.render_modes = ["Flat", "ColorInterp", "Phong", "Gouraud", "Texture"]
        self.render_mode_idx = 0
        
        self.is_wireframe = False

    def get_params_values(self):
        all_params = {key: param.value for key, param in self.params.items()}
        all_params.update({key: param.value for key, param in self.material_params.items()})
        
        all_params["render_mode"] = self.render_modes[self.render_mode_idx]
        return all_params
    
    def get_transform_values(self):
        return {key: param.value for key, param in self.transform_params.items()}