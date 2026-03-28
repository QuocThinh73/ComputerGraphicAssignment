from ..base_state import BaseState, FloatParam, ColorParam


class TorusState(BaseState):
    def __init__(self):
        super().__init__("Tetrahedron")
        self.params = {
            "major_radius": FloatParam("Major Radius", 1.0),
            "minor_radius": FloatParam("Minor Radius", 0.3),
            "color": ColorParam("Color", (0.0, 0.0, 1.0)),
        }