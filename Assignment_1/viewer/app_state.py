from configs import *
from libs.lighting import Light
from libs.camera import Camera
from states import *

class AppState:
    def __init__(self):
        self.APP_MODE_SCENE = 0
        self.APP_MODE_SGD = 1
        self.current_app_mode = self.APP_MODE_SCENE
        
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
        
        self.show_grid_x = DEFAULT_SHOW_GRID_X
        self.show_grid_y = DEFAULT_SHOW_GRID_Y
        self.show_grid_z = DEFAULT_SHOW_GRID_Z
        
        self.grid_need_rebuild = False
        
        self.cameras = []
        self.add_camera()
        
        self.lights = []

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
            
    def add_camera(self):
        new_cam = Camera(
            yaw=DEFAULT_CAM_YAW, 
            pitch=DEFAULT_CAM_PITCH, 
            distance=DEFAULT_CAM_DISTANCE
        )
        self.cameras.append(new_cam)
        self.active_camera_idx = len(self.cameras) - 1

    def remove_camera(self, idx):
        if len(self.cameras) > 1:
            self.cameras.pop(idx)
            if self.active_camera_idx >= len(self.cameras):
                self.active_camera_idx = len(self.cameras) - 1
                
    def add_light(self):
        new_light = Light(
            position=DEFAULT_LIGHT_POS,
            diffuse=DEFAULT_LIGHT_DIFFUSE,
            specular=DEFAULT_LIGHT_SPECULAR,
            ambient=DEFAULT_LIGHT_AMBIENT
        )
        new_light.enabled = True
        self.lights.append(new_light)

    def remove_light(self, idx):
        if 0 <= idx < len(self.lights):
            self.lights.pop(idx)