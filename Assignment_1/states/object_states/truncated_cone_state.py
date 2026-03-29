from ..base_state import BaseState, FloatParam, ColorParam
from configs import *


class TruncatedConeState(BaseState):
    def __init__(self):
        super().__init__("Truncated Cone")
        self.params = {
            "bottom_radius": FloatParam("Bottom radius", DEFAULT_TRUNCATED_CONE_BOTTOM_RADIUS),
            "top_radius": FloatParam("Top radius", DEFAULT_TRUNCATED_CONE_TOP_RADIUS),
            "height": FloatParam("Height", DEFAULT_TRUNCATED_CONE_HEIGHT),
            "color": ColorParam("Color", DEFAULT_COLOR),
        }