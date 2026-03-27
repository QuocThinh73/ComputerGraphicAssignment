from ..base_state import ObjectState, FloatParam


class HexagonState(ObjectState):
    def __init__(self):
        super().__init__("Hexagon")
        self.params = {
            "radius": FloatParam("Radius", 0.5),
        }