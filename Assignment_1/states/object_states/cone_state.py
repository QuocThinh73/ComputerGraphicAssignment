from ..base_state import BaseState, FloatParam, ColorParam
from configs import *


class ConeState(BaseState):
    def __init__(self):
        super().__init__("Cone")
        self.params = {
            "radius": FloatParam("Radius", 0.5),
            "height": FloatParam("Height", 1.0),
            "color": ColorParam("Color", DEFAULT_COLOR),
        }