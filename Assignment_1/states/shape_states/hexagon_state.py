from ..base_state import BaseState, FloatParam


class HexagonState(BaseState):
    def __init__(self):
        super().__init__("Hexagon")
        self.params = {
            "radius": FloatParam("Radius", 0.5),
        }