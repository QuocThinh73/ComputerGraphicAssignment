from ..base_state import ObjectState, Parameter


class TruncatedConeState(ObjectState):
    def __init__(self):
        super().__init__("Truncated Cone")
        self.params = {
            "bottom_radius": Parameter("Bottom radius", 0.8),
            "top_radius": Parameter("Top radius", 0.3),
            "height": Parameter("Height", 1.0),
        }