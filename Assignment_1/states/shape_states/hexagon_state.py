from ..base_state import BaseState, FloatParam, ColorParam


class HexagonState(BaseState):
    def __init__(self):
        super().__init__("Hexagon")
        self.params = {
            "radius": FloatParam("Radius", 0.5),
            "color": ColorParam("Color", (0.0, 0.0, 1.0)),
        }