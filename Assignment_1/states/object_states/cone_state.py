from ..base_state import BaseState, FloatParam
from configs import *


class ConeState(BaseState):
    def __init__(self):
        super().__init__("Cone")
        self.params = {
            "radius": FloatParam("Radius", DEFAULT_CONE_RADIUS),
            "height": FloatParam("Height", DEFAULT_CONE_HEIGHT),
        }