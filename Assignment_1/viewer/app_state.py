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
        
        self.shader_names = [
            "Flat",
            "ColorInterp",
            "Phong",
            "Gouraud",
        ]

        self.shape_index = self.shape_names.index("Rectangle")
        self.shader_name = "ColorInterp"
        self.need_rebuild_model = True
        
        # default params
        ## rectangle
        self.rectangle_width = 2.0
        self.rectangle_height = 1.0

    @property
    def current_shape_name(self):
        return self.shape_names[self.shape_index]