from ..base_state import BaseState, FloatParam


class CircleState(BaseState):
    def __init__(self):
        super().__init__("Circle")
        self.params = {
            "radius": FloatParam("Radius", 0.5),
        }