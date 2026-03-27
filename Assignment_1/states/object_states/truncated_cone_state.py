from ..base_state import ObjectState, FloatParam


class TruncatedConeState(ObjectState):
    def __init__(self):
        super().__init__("Truncated Cone")
        self.params = {
            "bottom_radius": FloatParam("Bottom radius", 0.8),
            "top_radius": FloatParam("Top radius", 0.3),
            "height": FloatParam("Height", 1.0),
        }