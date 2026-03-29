from ..base_state import BaseState, FloatParam, ColorParam
from configs import *


class TrapeziumState(BaseState):
    def __init__(self):
        super().__init__("Trapezium")
        self.params = {
            "bottom_width": FloatParam("Bottom Width", 2.5),
            "top_width": FloatParam("Top Width", 1.0),
            "height": FloatParam("Height", 1.0),
            "color": ColorParam("Color", DEFAULT_COLOR),
        }