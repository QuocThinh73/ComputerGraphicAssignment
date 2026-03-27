from ..base_state import ObjectState, Parameter


class CylinderState(ObjectState):
    def __init__(self):
        super().__init__("Cylinder")
        self.params = {
            "radius": Parameter("Radius", 1.0),
            "height": Parameter("Height", 1.0),
        }