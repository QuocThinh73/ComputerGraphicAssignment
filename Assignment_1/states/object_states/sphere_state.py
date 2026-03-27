from ..base_state import BaseState, FloatParam, IntParam


class Sphere1State(BaseState):
    def __init__(self):
        super().__init__("UVSphere")
        self.params = {
            "radius": FloatParam("Radius", 0.5),
            "sectors": IntParam("Sectors", 36),
            "stacks": IntParam("Stacks", 18),
        }


class Sphere2State(BaseState):
    def __init__(self):
        super().__init__("CubedSphere")
        self.params = {
            "radius": FloatParam("Radius", 0.5),
            "segments": IntParam("Segments", 10),
        }


class Sphere3State(BaseState):
    def __init__(self):
        super().__init__("TetraSphere")
        self.params = {
            "radius": FloatParam("Radius", 0.5),
            "subdivisions": IntParam("Subdivisions", 3, min_val=0, max_val=10),
        }