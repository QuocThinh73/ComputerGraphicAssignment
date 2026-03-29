from ..base_state import BaseState, ColorParam, FloatParam, StringParam


class FunctionGraphState(BaseState):
    def __init__(self):
        super().__init__("FunctionGraph")
        self.params = {
            "func_str": StringParam("Function", ""),
            "min_x": FloatParam("Min X", -5.0, -20.0, 0.0),
            "max_x": FloatParam("Max X", 5.0, 0.0, 20.0),
            "min_y": FloatParam("Min Y", -5.0, -20.0, 0.0),
            "max_y": FloatParam("Max Y", 5.0, 0.0, 20.0),
            "delta_x": FloatParam("Delta X", 0.2, 0.05, 2.0),
            "delta_y": FloatParam("Delta Y", 0.2, 0.05, 2.0),
            "color": ColorParam("Color", (0.0, 0.0, 1.0))
        }