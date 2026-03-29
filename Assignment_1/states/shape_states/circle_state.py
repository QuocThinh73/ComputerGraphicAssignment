from ..base_state import BaseState, FloatParam
from configs import *


class CircleState(BaseState):
    def __init__(self):
        super().__init__("Circle")
        self.params = {
            "radius": FloatParam("Radius", DEFAULT_CIRCLE_RADIUS),
        }