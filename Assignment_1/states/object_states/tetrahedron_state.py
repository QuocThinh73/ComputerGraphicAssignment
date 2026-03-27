from ..base_state import ObjectState, FloatParam


class TetrahedronState(ObjectState):
    def __init__(self):
        super().__init__("Tetrahedron")
        self.params = {
            "size": FloatParam("Size", 0.5),
        }