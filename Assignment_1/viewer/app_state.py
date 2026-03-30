from configs import *
from libs.lighting import Light
from libs.camera import Camera
from states import *

class AppState:
    def __init__(self):
        self.APP_MODE_SCENE = 0
        self.APP_MODE_SGD = 1
        self.current_app_mode = self.APP_MODE_SCENE
        
        # ==========================================
        # SCENE BUILDER MODE
        # ==========================================
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
        
        # ==========================================
        # SGD VISUALIZER MODE
        # ==========================================
        self.sgd_functions = [
            {
                "name": "Quadratic 2D",
                "formula": "x**2 + y**2",
                "min_x": -2.0, "max_x": 2.0, "min_y": -2.0, "max_y": 2.0, "delta": 0.1
            },
            {
                "name": "Himmelblau",
                "formula": "(x**2 + y - 11)**2 + (x + y**2 - 7)**2",
                "min_x": -2.0, "max_x": 2.0, "min_y": -2.0, "max_y": 2.0, "delta": 0.1
            },
            {
                "name": "Rosenbrock (a=1, b=100)",
                "formula": "(1 - x)**2 + 100 * (y - x**2)**2",
                "min_x": -2.0, "max_x": 2.0, "min_y": -2.0, "max_y": 2.0, "delta": 0.1
            },
            {
                "name": "Booth",
                "formula": "(x + 2*y - 7)**2 + (2*x + y - 5)**2",
                "min_x": -2.0, "max_x": 2.0, "min_y": -2.0, "max_y": 2.0, "delta": 0.1
            }
        ]
        self.sgd_func_names = [f["name"] for f in self.sgd_functions]
        self.sgd_selected_func_idx = 0
        self.sgd_surface_need_rebuild = True
        
        self.sgd_algorithms = ["Gradient Descent", "SGD", "Mini-batch SGD", "Momentum", "Adam"]
        self.sgd_algo_idx = 0
        
        self.sgd_learning_rate = 0.01
        self.sgd_momentum = 0.9
        self.sgd_epochs = 100
        self.sgd_sim_speed = 1.0
        
        self.sgd_is_playing = False

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