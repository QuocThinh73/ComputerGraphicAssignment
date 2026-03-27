class Parameter:
    def __init__(self, label, value, min_val=0.1, max_val=10.0):
        self.label = label
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        
        
class RectangleState:
    def __init__(self):
        self.name = "Rectangle"
        self.params = {
            "width": Parameter("Width", 1.0),
            "height": Parameter("Height", 0.5),
        }
        
    def get_params_values(self):
        return {key: param.value for key, param in self.params.items()}
    
    
class CubeState:
    def __init__(self):
        self.name = "Cube"
        self.params = {
            "width": Parameter("Width", 1.0),
            "height": Parameter("Height", 1.0),
            "depth": Parameter("Depths", 1.0),
        }
        
    def get_params_values(self):
        return {key: param.value for key, param in self.params.items()}
    

class AppState:
    def __init__(self):
        self.states = {
            # "Triangle": TriangleState(),
            "Rectangle": RectangleState(),
            # "Pentagon",
            # "Hexagon",
            # "Circle",
            # "Elip",
            # "Trapezium",
            # "Star",
            "Cube": CubeState(),
            # "Cylinder",
            # "Cone",
            # "TruncatedCone",
            # "Prism",
            # "Torus",
            # "Tetrahedron",
            # "FunctionGraph",
        }
        
        self.shader_names = [
            "Flat",
            "ColorInterp",
            "Phong",
            "Gouraud",
        ]
        
        self.shape_names = list(self.states.keys())
        self.shape_index = self.shape_names.index("Rectangle")
        self.shader_name = "ColorInterp"
        self.need_rebuild_model = True

    @property
    def current_shape_name(self):
        return self.shape_names[self.shape_index]
    
    @property
    def current_state(self):
        return self.states[self.current_shape_name]