from ..base_state import BaseState, FloatParam, ColorParam


class ArrowState(BaseState):
    def __init__(self):
        super().__init__("Arrow")
        self.params = {
            "shaft_width": FloatParam("Shaft Width", 0.5),
            "shaft_length": FloatParam("Shaft Length", 1.5),
            "head_width": FloatParam("Head Width", 1.5),
            "head_length": FloatParam("Head Length", 1.0),
            "color": ColorParam("Color", (0.0, 0.0, 1.0)),
        }