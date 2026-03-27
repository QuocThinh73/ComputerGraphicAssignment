from ..base_state import ObjectState, Parameter

class CircleState(ObjectState):
    def __init__(self):
        super().__init__("Circle")
        self.params = {
            "radius": Parameter("Radius", 1.0),
        }