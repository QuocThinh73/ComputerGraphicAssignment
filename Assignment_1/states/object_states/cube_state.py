from ..base_state import ObjectState, FloatParam


class CubeState(ObjectState):
    def __init__(self):
        super().__init__("Cube")
        self.params = {
            "width": FloatParam("Width", 1.0),
            "height": FloatParam("Height", 1.0),
            "depth": FloatParam("Depth", 1.0),
        }