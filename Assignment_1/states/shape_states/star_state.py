from ..base_state import ObjectState, FloatParam


class StarState(ObjectState):
    def __init__(self):
        super().__init__("Star")
        self.params = {
            "short_radius": FloatParam("Short Radius", 0.35),
            "long_radius": FloatParam("Long Radius", 0.9),
        }