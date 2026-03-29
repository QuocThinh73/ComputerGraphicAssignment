from ..base_state import BaseState, FloatParam, ColorParam
from configs import *


class TorusState(BaseState):
    def __init__(self):
        super().__init__("Tetrahedron")
        self.params = {
            "major_radius": FloatParam("Major Radius", 1.0),
            "minor_radius": FloatParam("Minor Radius", 0.3),
            "color": ColorParam("Color", DEFAULT_COLOR),
        }