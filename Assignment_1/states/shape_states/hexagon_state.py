from ..base_state import BaseState, FloatParam
from configs import *


class HexagonState(BaseState):
    def __init__(self):
        super().__init__("Hexagon")
        self.params = {
            "radius": FloatParam("Radius", DEFAULT_HEXAGON_RADIUS),
        }