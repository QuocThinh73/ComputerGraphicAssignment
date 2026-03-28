from ..base_state import BaseState, FloatParam, ColorParam


class CylinderState(BaseState):
    def __init__(self):
        super().__init__("Cylinder")
        self.params = {
            "radius": FloatParam("Radius", 1.0),
            "height": FloatParam("Height", 1.0),
            "color": ColorParam("Color", (0.0, 0.0, 1.0)),
        }