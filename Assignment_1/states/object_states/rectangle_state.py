from ..base_state import ObjectState, Parameter

class RectangleState(ObjectState):
    def __init__(self):
        super().__init__("Rectangle")
        self.params = {
            "width": Parameter("Width", 1.0),
            "height": Parameter("Height", 0.5),
        }