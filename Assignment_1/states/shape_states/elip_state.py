from ..base_state import BaseState, FloatParam, ColorParam


class ElipState(BaseState):
    def __init__(self):
        super().__init__("Elip")
        self.params = {
            "width": FloatParam("Width", 0.5),
            "height": FloatParam("Height", 1.0),
            "color": ColorParam("Color", (0.0, 0.0, 1.0)),
        }