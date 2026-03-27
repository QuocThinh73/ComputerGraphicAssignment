from ..base_state import ObjectState, Parameter

class CubeState(ObjectState):
    def __init__(self):
        super().__init__("Cube")
        self.params = {
            "width": Parameter("Width", 1.0),
            "height": Parameter("Height", 1.0),
            "depth": Parameter("Depth", 1.0),
        }