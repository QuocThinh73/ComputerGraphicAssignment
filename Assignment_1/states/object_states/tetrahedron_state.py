from ..base_state import BaseState, FloatParam, ColorParam
from configs import *


class TetrahedronState(BaseState):
    def __init__(self):
        super().__init__("Tetrahedron")
        self.params = {
            "size": FloatParam("Size", 0.5),
            "color": ColorParam("Color", DEFAULT_COLOR),
        }