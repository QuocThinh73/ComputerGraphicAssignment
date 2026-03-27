from ..base_state import ObjectState, FloatParam


class TriangleState(ObjectState):
    def __init__(self):
        super().__init__("Triangle")
        self.params = {
            "base": FloatParam("Base", 1.0),
            "height": FloatParam("Height", 0.5),
        }