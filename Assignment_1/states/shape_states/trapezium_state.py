from ..base_state import BaseState, FloatParam
from configs import *


class TrapeziumState(BaseState):
    def __init__(self):
        super().__init__("Trapezium")
        self.params = {
            "bottom_width": FloatParam("Bottom Width", DEFAULT_BOTTOM_WIDTH),
            "top_width": FloatParam("Top Width", DEFAULT_TOP_WIDTH),
            "height": FloatParam("Height", DEFAULT_HEIGHT),
        }