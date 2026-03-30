from models import *


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
    "ImportedModel": ImportedModel,
    # Function graph
    "FunctionGraph": FunctionGraphModel,
}

def build_shape(shape_name: str, **kwargs):
    shape_cls = SHAPE_CLASSES[shape_name]
    model = shape_cls(**kwargs).setup()
    return model