class AppState:
    def __init__(self):
        self.shape_names = [
            "Triangle",
            "Rectangle",
            "Pentagon",
            "Hexagon",
            "Circle",
            "Elip",
            "Trapezium",
            "Star",
            "Cube",
            "Cylinder",
            "Cone",
            "TruncatedCone",
            "Prism",
            "Torus",
            "Tetrahedron",
            "FunctionGraph",
        ]

        self.shape_index = self.shape_names.index("Cube")

        self.shader_name = "color_interp"

        self.need_rebuild_model = True

    @property
    def current_shape_name(self):
        return self.shape_names[self.shape_index]