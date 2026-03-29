from ..base_state import BaseState, FloatParam
from configs import *


class StarState(BaseState):
    def __init__(self):
        super().__init__("Star")
        self.params = {
            "short_radius": FloatParam("Short Radius", DEFAULT_STAR_SHORT_RADIUS),
            "long_radius": FloatParam("Long Radius", DEFAULT_STAR_LONG_RADIUS),
        }