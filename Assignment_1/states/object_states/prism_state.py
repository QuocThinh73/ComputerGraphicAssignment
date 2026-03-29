from ..base_state import BaseState, FloatParam, IntParam, ColorParam
from configs import *


class PrismState(BaseState):
    def __init__(self):
        super().__init__("Prism")
        self.params = {
            "radius": FloatParam("Radius", DEFAULT_PRISM_RADIUS),
            "height": FloatParam("Height", DEFAULT_PRISM_HEIGHT),
            "num_sides": IntParam("Num sides", DEFAULT_PRISM_NUM_SIDES, 3, 12),
            "color": ColorParam("Color", DEFAULT_COLOR),
        }