from ..base_state import BaseState, FloatParam, ColorParam


class StarState(BaseState):
    def __init__(self):
        super().__init__("Star")
        self.params = {
            "short_radius": FloatParam("Short Radius", 0.35),
            "long_radius": FloatParam("Long Radius", 0.9),
            "color": ColorParam("Color", (0.0, 0.0, 1.0)),
        }