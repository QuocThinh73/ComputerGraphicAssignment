from pathlib import Path

from models import *

BASE_DIR = Path(__file__).resolve().parent.parent
SHADERS_DIR = BASE_DIR / "shaders"


SHAPE_CLASSES = {
    # 2D
    "Triangle": TriangleModel,
    "Rectangle": RectangleModel,
    "Trapezium": TrapeziumModel,
    "Pentagon": PentagonModel,
    "Hexagon": HexagonModel,
    "Circle": CircleModel,
    "Elip": ElipModel,
    "Star": StarModel,
    "Arrow": ArrowModel,
    # 3D
    "Cube": CubeModel,
    "Cone": ConeModel,
    "TruncatedCone": TruncatedConeModel,
    "Cylinder": CylinderModel,
    "Tetrahedron": TetrahedronModel,
    "Torus": TorusModel,
    "Prism": PrismModel,
    "Sphere1": Sphere1Model,
    "Sphere2": Sphere2Model,
    "Sphere3": Sphere3Model,
    # Function graph
    "FunctionGraph": FunctionGraphModel,
}


SHADER_FILES = {
    "ColorInterp": (
        str(SHADERS_DIR / "color_interp.vert"),
        str(SHADERS_DIR / "color_interp.frag"),
    ),
    "Flat": (
        str(SHADERS_DIR / "flat.vert"),
        str(SHADERS_DIR / "flat.frag"),
    ),
    "Gouraud": (
        str(SHADERS_DIR / "gouraud.vert"),
        str(SHADERS_DIR / "gouraud.frag"),
    ),
    "Phong": (
        str(SHADERS_DIR / "phong.vert"),
        str(SHADERS_DIR / "phong.frag"),
    ),
    "Texture": (
        str(SHADERS_DIR / "texture.vert"),
        str(SHADERS_DIR / "texture.frag"),
    )
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