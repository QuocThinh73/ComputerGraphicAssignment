from ..base_state import BaseState, FloatParam
from configs import *


class TriangleState(BaseState):
    def __init__(self):
        super().__init__("Triangle")
        self.params = {
            "base": FloatParam("Base", DEFAULT_TRIANGLE_BASE),
            "height": FloatParam("Height", DEFAULT_TRIANGLE_HEIGHT),
        }