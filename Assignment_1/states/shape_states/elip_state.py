from ..base_state import ObjectState, FloatParam


class ElipState(ObjectState):
    def __init__(self):
        super().__init__("Elip")
        self.params = {
            "width": FloatParam("Width", 0.5),
            "height": FloatParam("Height", 1.0),
        }