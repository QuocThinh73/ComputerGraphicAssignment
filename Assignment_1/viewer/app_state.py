from states import *


class AppState:
    def __init__(self):
        self.states = {
            # 2D
            "Triangle": TriangleState(),
            "Rectangle": RectangleState(),
            "Trapezium": TrapeziumState(),
            "Pentagon": PentagonState(),
            "Hexagon": HexagonState(),
            "Circle": CircleState(),
            "Elip": ElipState(),
            "Star": StarState(),
            "Arrow": ArrowState(),
            # 3D
            "Cube": CubeState(),
            "Cone": ConeState(),
            "TruncatedCone": TruncatedConeState(),
            "Cylinder": CylinderState(),
            "Tetrahedron": TetrahedronState(),
            "Torus": TorusState(),
            "Prism": PrismState(),
            "Sphere1": Sphere1State(),
            "Sphere2": Sphere2State(),
            "Sphere3": Sphere3State(),
        }
        
        self.shader_names = [
            "Flat",
            "ColorInterp",
            "Phong",
            "Gouraud",
        ]
        
        self.shape_names = list(self.states.keys())
        self.shape_index = self.shape_names.index("Rectangle")
        self.shader_name = "ColorInterp"
        self.need_rebuild_model = True

    @property
    def current_shape_name(self):
        return self.shape_names[self.shape_index]
    
    @property
    def current_state(self):
        return self.states[self.current_shape_name]