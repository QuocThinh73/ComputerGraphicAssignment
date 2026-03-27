from ..base_state import BaseState, FloatParam, IntParam


class PrismState(BaseState):
    def __init__(self):
        super().__init__("Prism")
        self.params = {
            "radius": FloatParam("Radius", 1.0),
            "height": FloatParam("Height", 1.0),
            "num_sides": IntParam("Num sides", 3),
        }