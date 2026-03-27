from ..base_state import ObjectState, FloatParam


class TrapeziumState(ObjectState):
    def __init__(self):
        super().__init__("Trapezium")
        self.params = {
            "bottom_width": FloatParam("Bottom Width", 2.5),
            "top_width": FloatParam("Top Width", 1.0),
            "height": FloatParam("Height", 1.0),
        }