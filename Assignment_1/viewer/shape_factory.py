from pathlib import Path

from models import RectangleModel, CubeModel, CircleModel

BASE_DIR = Path(__file__).resolve().parent.parent
SHADERS_DIR = BASE_DIR / "shaders"


SHAPE_CLASSES = {
    "Rectangle": RectangleModel,
    "Circle": CircleModel,
    "Cube": CubeModel,
}


SHADER_FILES = {
    "ColorInterp": (
        str(SHADERS_DIR / "color_interp.vert"),
        str(SHADERS_DIR / "color_interp.frag"),
    ),
    # "Flat": (
    #     str(BASICSHAPE_DIR / "flat.vert"),
    #     str(BASICSHAPE_DIR / "flat.frag"),
    # ),
    # "Gouraud": (
    #     str(BASICSHAPE_DIR / "gouraud.vert"),
    #     str(BASICSHAPE_DIR / "gouraud.frag"),
    # ),
    # "Phong": (
    #     str(BASICSHAPE_DIR / "phong.vert"),
    #     str(BASICSHAPE_DIR / "phong.frag"),
    # ),
}


def build_shape(shape_name: str, shader_name: str, **kwargs):
    shape_cls = SHAPE_CLASSES[shape_name]
    vert_path, frag_path = SHADER_FILES[shader_name]

    model = shape_cls(
        vert_path, 
        frag_path, 
        **kwargs
    ).setup()

    return model