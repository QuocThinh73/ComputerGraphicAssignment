from ..base_state import BaseState, FloatParam
from configs import *

class CubeState(BaseState):
    def __init__(self):
        super().__init__("Cube")
        self.params = {
            "width": FloatParam("Width", DEFAULT_CUBE_WIDTH),
            "height": FloatParam("Height", DEFAULT_CUBE_HEIGHT),
            "depth": FloatParam("Depth", DEFAULT_CUBE_DEPTH),
        }