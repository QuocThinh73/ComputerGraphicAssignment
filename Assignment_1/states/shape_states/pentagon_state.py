from ..base_state import ObjectState, FloatParam


class PentagonState(ObjectState):
    def __init__(self):
        super().__init__("Pentagon")
        self.params = {
            "radius": FloatParam("Radius", 0.5),
        }