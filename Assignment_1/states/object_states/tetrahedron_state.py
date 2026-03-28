from ..base_state import BaseState, FloatParam, ColorParam


class TetrahedronState(BaseState):
    def __init__(self):
        super().__init__("Tetrahedron")
        self.params = {
            "size": FloatParam("Size", 0.5),
            "color": ColorParam("Color", (0.0, 0.0, 1.0)),
        }