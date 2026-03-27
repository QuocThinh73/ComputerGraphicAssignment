from ..base_state import BaseState, FloatParam


class RectangleState(BaseState):
    def __init__(self):
        super().__init__("Rectangle")
        self.params = {
            "width": FloatParam("Width", 1.0),
            "height": FloatParam("Height", 0.5),
        }