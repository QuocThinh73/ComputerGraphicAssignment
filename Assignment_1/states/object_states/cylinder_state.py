from ..base_state import BaseState, FloatParam, ColorParam
from configs import *


class CylinderState(BaseState):
    def __init__(self):
        super().__init__("Cylinder")
        self.params = {
            "radius": FloatParam("Radius", 1.0),
            "height": FloatParam("Height", 1.0),
            "color": ColorParam("Color", DEFAULT_COLOR),
        }