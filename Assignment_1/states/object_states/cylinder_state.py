from ..base_state import BaseState, FloatParam, ColorParam
from configs import *


class CylinderState(BaseState):
    def __init__(self):
        super().__init__("Cylinder")
        self.params = {
            "radius": FloatParam("Radius", DEFAULT_CYLINDER_RADIUS),
            "height": FloatParam("Height", DEFAULT_CYLINDER_HEIGHT),
            "color": ColorParam("Color", DEFAULT_COLOR),
        }