from ..base_state import BaseState, FloatParam, ColorParam


class CubeState(BaseState):
    def __init__(self):
        super().__init__("Cube")
        self.params = {
            "width": FloatParam("Width", 1.0),
            "height": FloatParam("Height", 1.0),
            "depth": FloatParam("Depth", 1.0),
            "color": ColorParam("Color", (0.0, 0.0, 1.0))
        }