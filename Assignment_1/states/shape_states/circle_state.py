from ..base_state import ObjectState, FloatParam


class CircleState(ObjectState):
    def __init__(self):
        super().__init__("Circle")
        self.params = {
            "radius": FloatParam("Radius", 0.5),
        }