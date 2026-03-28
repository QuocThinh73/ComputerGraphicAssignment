from ..base_state import BaseState, FloatParam, ColorParam


class RectangleState(BaseState):
    def __init__(self):
        super().__init__("Rectangle")
        self.params = {
            "width": FloatParam("Width", 1.0),
            "height": FloatParam("Height", 0.5),
            "color": ColorParam("Color", (0.0, 0.0, 1.0)),
        }