from ..base_state import ObjectState, Parameter


class ConeState(ObjectState):
    def __init__(self):
        super().__init__("Cone")
        self.params = {
            "radius": Parameter("Radius", 0.5),
            "height": Parameter("Height", 1.0),
        }