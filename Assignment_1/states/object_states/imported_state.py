from ..base_state import BaseState, FloatParam, StringParam
from configs import *


class ImportedState(BaseState):
    def __init__(self):
        super().__init__("ImportedModel")
        self.params = {
            "file_path": StringParam("File Path", "assets/bunny.obj"), 
            "scale_factor": FloatParam("Scale Size", 2.0, 0.1, 10.0),
        }