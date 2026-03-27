from ..base_state import ObjectState, FloatParam


class RectangleState(ObjectState):
    def __init__(self):
        super().__init__("Rectangle")
        self.params = {
            "width": FloatParam("Width", 1.0),
            "height": FloatParam("Height", 0.5),
        }