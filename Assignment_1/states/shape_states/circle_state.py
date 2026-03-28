from ..base_state import BaseState, FloatParam, ColorParam


class CircleState(BaseState):
    def __init__(self):
        super().__init__("Circle")
        self.params = {
            "radius": FloatParam("Radius", 0.5),
            "color": ColorParam("Color", (0.0, 0.0, 1.0)),
        }