from ..base_state import ObjectState, FloatParam


class TorusState(ObjectState):
    def __init__(self):
        super().__init__("Tetrahedron")
        self.params = {
            "major_radius": FloatParam("Major Radius", 1.0),
            "minor_radius": FloatParam("Minor Radius", 0.3),
        }