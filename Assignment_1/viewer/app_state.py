from states import *

class AppState:
    def __init__(self):
        self.blueprints = {
            # 2D
            "Triangle": TriangleState,
            "Rectangle": RectangleState,
            "Trapezium": TrapeziumState,
            "Pentagon": PentagonState,
            "Hexagon": HexagonState,
            "Circle": CircleState,
            "Elip": ElipState,
            "Star": StarState,
            "Arrow": ArrowState,
            # 3D
            "Cube": CubeState,
            "Cone": ConeState,
            "TruncatedCone": TruncatedConeState,
            "Cylinder": CylinderState,
            "Tetrahedron": TetrahedronState,
            "Torus": TorusState,
            "Prism": PrismState,
            "Sphere1": Sphere1State,
            "Sphere2": Sphere2State,
            "Sphere3": Sphere3State,
            # Function graph
            "FunctionGraph": FunctionGraphState
        }
        
        self.available_types = list(self.blueprints.keys())
        self.selected_add_index = self.available_types.index("Cube")
        
        self.scene_objects = []
        self.next_obj_id = 1
        self.selected_obj_id = None
        
        self.show_grid_x = True
        self.show_grid_y = False
        self.show_grid_z = True
        
        self.grid_need_rebuild = False

    def add_object(self, obj_type):
        if obj_type in self.blueprints:
            new_state = self.blueprints[obj_type]() 
            new_obj = {
                "id": self.next_obj_id,
                "type": obj_type,
                "name": f"{obj_type} {self.next_obj_id}",
                "state": new_state,
                "model": None,
                "need_rebuild": True
            }
            self.scene_objects.append(new_obj)
            self.selected_obj_id = self.next_obj_id
            self.next_obj_id += 1

    def remove_object(self, obj_id):
        self.scene_objects = [obj for obj in self.scene_objects if obj["id"] != obj_id]
        if self.selected_obj_id == obj_id:
            self.selected_obj_id = None