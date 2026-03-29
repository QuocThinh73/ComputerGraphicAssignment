from ..base_state import BaseState, FloatParam, IntParam
from configs import *


class TorusState(BaseState):
    def __init__(self):
        super().__init__("Torus")
        self.params = {
            "major_radius": FloatParam("Major Radius", DEFAULT_TORUS_MAJOR_RADIUS),
            "minor_radius": FloatParam("Minor Radius", DEFAULT_TORUS_MINOR_RADIUS),
            "major_segments": IntParam("Major Segments", DEFAULT_TORUS_MAJOR_SEGMENTS, 3, 360),
            "minor_segments": IntParam("Minor Segments", DEFAULT_TORUS_MINOR_SEGMENTS, 3, 360),
        }