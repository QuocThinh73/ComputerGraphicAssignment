from ..base_state import BaseState, FloatParam
from configs import *


class ArrowState(BaseState):
    def __init__(self):
        super().__init__("Arrow")
        self.params = {
            "shaft_width": FloatParam("Shaft Width", DEFAULT_ARROW_SHAFT_WIDTH),
            "shaft_length": FloatParam("Shaft Length", DEFAULT_ARROW_SHAFT_LENGTH),
            "head_width": FloatParam("Head Width", DEFAULT_ARROW_HEAD_WIDTH),
            "head_length": FloatParam("Head Length", DEFAULT_ARROW_HEAD_LENGTH),
        }