from ..base_state import BaseState, FloatParam, ColorParam, StringParam
from configs import *


class CubeState(BaseState):
    def __init__(self):
        super().__init__("Cube")
        self.params = {
            # Object properties
            "width": FloatParam("Width", DEFAULT_CUBE_WIDTH),
            "height": FloatParam("Height", DEFAULT_CUBE_HEIGHT),
            "depth": FloatParam("Depth", DEFAULT_CUBE_DEPTH),
            # Flat color mode
            "color": ColorParam("Color", DEFAULT_COLOR),
            # Phong & Gouraud modes
            "diffuse": ColorParam("Diffuse", DEFAULT_MAT_DIFFUSE),
            "specular": ColorParam("Specular", DEFAULT_MAT_SPECULAR),
            "ambient": ColorParam("Ambient", DEFAULT_MAT_AMBIENT),
            "shininess": FloatParam("Shininess", DEFAULT_MAT_SHININESS, 1.0, 128.0),
            # Texture mode
            "texture_path": StringParam("Texture Path", ""),
        }