from ..base_state import BaseState, FloatParam
from configs import *


class ElipState(BaseState):
    def __init__(self):
        super().__init__("Elip")
        self.params = {
            "width": FloatParam("Width", DEFAULT_ELLIPSE_WIDTH),
            "height": FloatParam("Height", DEFAULT_ELLIPSE_HEIGHT),
        }