from pathlib import Path

from BasicShape import Triangle, Rectangle, Pentagon, Hexagon, Circle, Elip, Trapezium, Star
from BasicShape import Cube, Cylinder, Cone, TruncatedCone, Prism, Torus, Tetrahedron
from BasicShape import FunctionGraph


BASE_DIR = Path(__file__).resolve().parent.parent
BASICSHAPE_DIR = BASE_DIR / "BasicShape"


SHAPE_CLASSES = {
    "Triangle": Triangle,
    "Rectangle": Rectangle,
    "Pentagon": Pentagon,
    "Hexagon": Hexagon,
    "Circle": Circle,
    "Elip": Elip,
    "Trapezium": Trapezium,
    "Star": Star,
    "Cube": Cube,
    "Cylinder": Cylinder,
    "Cone": Cone,
    "TruncatedCone": TruncatedCone,
    "Prism": Prism,
    "Torus": Torus,
    "Tetrahedron": Tetrahedron,
    "FunctionGraph": FunctionGraph,
}


SHADER_FILES = {
    "ColorInterp": (
        str(BASICSHAPE_DIR / "color_interp.vert"),
        str(BASICSHAPE_DIR / "color_interp.frag"),
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


def build_shape(shape_name: str, shader_name: str, state=None):
    if shape_name not in SHAPE_CLASSES:
        raise ValueError(f"Unknown shape: {shape_name}")

    if shader_name not in SHADER_FILES:
        raise ValueError(f"Unknown shader: {shader_name}")

    shape_cls = SHAPE_CLASSES[shape_name]
    vert_path, frag_path = SHADER_FILES[shader_name]

    if shape_name == "Rectangle":
        model = shape_cls(
            vert_path,
            frag_path,
            width=state.rectangle_width,
            height=state.rectangle_height
        ).setup()
    else:
        model = shape_cls(vert_path, frag_path).setup()

    return model