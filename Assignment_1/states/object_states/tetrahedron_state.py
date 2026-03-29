from ..base_state import BaseState, FloatParam, ColorParam
from configs import *


class TetrahedronState(BaseState):
    def __init__(self):
        super().__init__("Tetrahedron")
        self.params = {
            "size": FloatParam("Size", DEFAULT_TETRAHEDRON_SIZE),
            "color": ColorParam("Color", DEFAULT_COLOR),
        }