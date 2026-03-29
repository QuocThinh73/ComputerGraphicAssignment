from ..base_state import BaseState, FloatParam, ColorParam
from configs import *


class HexagonState(BaseState):
    def __init__(self):
        super().__init__("Hexagon")
        self.params = {
            "radius": FloatParam("Radius", 0.5),
            "color": ColorParam("Color", DEFAULT_COLOR),
        }