from ..base_state import BaseState, FloatParam
from configs import *


class PentagonState(BaseState):
    def __init__(self):
        super().__init__("Pentagon")
        self.params = {
            "radius": FloatParam("Radius", DEFAULT_PENTAGON_RADIUS),
        }