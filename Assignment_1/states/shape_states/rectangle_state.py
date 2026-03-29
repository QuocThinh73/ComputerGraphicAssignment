from ..base_state import BaseState, FloatParam
from configs import *


class RectangleState(BaseState):
    def __init__(self):
        super().__init__("Rectangle")
        self.params = {
            "width": FloatParam("Width", DEFAULT_RECTANGLE_WIDTH),
            "height": FloatParam("Height", DEFAULT_RECTANGLE_HEIGHT),
        }