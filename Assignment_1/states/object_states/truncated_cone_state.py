from ..base_state import BaseState, FloatParam, ColorParam
from configs import *


class TruncatedConeState(BaseState):
    def __init__(self):
        super().__init__("Truncated Cone")
        self.params = {
            "bottom_radius": FloatParam("Bottom radius", 0.8),
            "top_radius": FloatParam("Top radius", 0.3),
            "height": FloatParam("Height", 1.0),
            "color": ColorParam("Color", DEFAULT_COLOR),
        }