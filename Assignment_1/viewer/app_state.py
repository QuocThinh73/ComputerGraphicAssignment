from states import RectangleState, CubeState, CircleState

class AppState:
    def __init__(self):
        self.states = {
            "Rectangle": RectangleState(),
            "Cube": CubeState(),
            "Circle": CircleState(),
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