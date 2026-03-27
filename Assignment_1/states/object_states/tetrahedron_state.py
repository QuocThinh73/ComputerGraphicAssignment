from ..base_state import BaseState, FloatParam


class TetrahedronState(BaseState):
    def __init__(self):
        super().__init__("Tetrahedron")
        self.params = {
            "size": FloatParam("Size", 0.5),
        }