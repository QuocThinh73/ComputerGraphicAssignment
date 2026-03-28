from ..base_state import BaseState, FloatParam, ColorParam


class TriangleState(BaseState):
    def __init__(self):
        super().__init__("Triangle")
        self.params = {
            "base": FloatParam("Base", 1.0),
            "height": FloatParam("Height", 0.5),
            "color": ColorParam("Color", (0.0, 0.0, 1.0)),
        }