from ..base_state import ObjectState, FloatParam


class ConeState(ObjectState):
    def __init__(self):
        super().__init__("Cone")
        self.params = {
            "radius": FloatParam("Radius", 0.5),
            "height": FloatParam("Height", 1.0),
        }