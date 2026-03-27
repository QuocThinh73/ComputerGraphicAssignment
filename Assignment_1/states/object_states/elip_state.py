from ..base_state import ObjectState, Parameter

class ElipState(ObjectState):
    def __init__(self):
        super().__init__("Elip")
        self.params = {
            "width": Parameter("Width", 0.5),
            "height": Parameter("Height", 1.0),
        }