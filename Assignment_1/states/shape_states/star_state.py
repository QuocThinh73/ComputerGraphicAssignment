from ..base_state import BaseState, FloatParam


class StarState(BaseState):
    def __init__(self):
        super().__init__("Star")
        self.params = {
            "short_radius": FloatParam("Short Radius", 0.35),
            "long_radius": FloatParam("Long Radius", 0.9),
        }