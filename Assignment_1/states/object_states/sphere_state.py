from ..base_state import BaseState, FloatParam, IntParam, ColorParam
from configs import *


class Sphere1State(BaseState):
    def __init__(self):
        super().__init__("UVSphere")
        self.params = {
            "radius": FloatParam("Radius", DEFAULT_SPHERE1_RADIUS),
            "sectors": IntParam("Sectors", DEFAULT_SPHERE1_SECTORS, 18, 360),
            "stacks": IntParam("Stacks", DEFAULT_SPHERE1_STACKS, 18, 360),
            "color": ColorParam("Color", DEFAULT_COLOR),
        }


class Sphere2State(BaseState):
    def __init__(self):
        super().__init__("CubedSphere")
        self.params = {
            "radius": FloatParam("Radius", DEFAULT_SPHERE2_RADIUS),
            "segments": IntParam("Segments", DEFAULT_SPHERE2_SEGMENTS, 1, 10),
            "color": ColorParam("Color", DEFAULT_COLOR),
        }


class Sphere3State(BaseState):
    def __init__(self):
        super().__init__("TetraSphere")
        self.params = {
            "radius": FloatParam("Radius", DEFAULT_SPHERE3_RADIUS),
            "subdivisions": IntParam("Subdivisions", DEFAULT_SPHERE3_SUBDIVISIONS, 0, 10),
            "color": ColorParam("Color", DEFAULT_COLOR),
        }