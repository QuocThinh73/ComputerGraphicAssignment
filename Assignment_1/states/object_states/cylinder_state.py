from ..base_state import ObjectState, FloatParam


class CylinderState(ObjectState):
    def __init__(self):
        super().__init__("Cylinder")
        self.params = {
            "radius": FloatParam("Radius", 1.0),
            "height": FloatParam("Height", 1.0),
        }