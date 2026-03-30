import numpy as np
from viewer.model_factory import build_shape
from models import GridFloorModel, FunctionGraphModel
import OpenGL.GL as GL


def create_translation_matrix(x, y, z):
    return np.array([
        [1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]
    ], dtype=np.float32)

def create_rotation_matrix_x(deg):
    rad = np.radians(deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]
    ], dtype=np.float32)

def create_rotation_matrix_y(deg):
    rad = np.radians(deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]
    ], dtype=np.float32)

def create_rotation_matrix_z(deg):
    rad = np.radians(deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]
    ], dtype=np.float32)

class Scene:
    def __init__(self, state):
        self.state = state
        
        self._init_scene_builder()
        self._init_sgd_visualizer()

    def update(self):
        if self.state.current_app_mode == self.state.APP_MODE_SCENE:
            self._update_scene_builder()
        elif self.state.current_app_mode == self.state.APP_MODE_SGD:
            self._update_sgd_visualizer()

    def draw(self, projection, view):
        if self.state.current_app_mode == self.state.APP_MODE_SCENE:
            self._draw_scene_builder(projection, view)
        elif self.state.current_app_mode == self.state.APP_MODE_SGD:
            self._draw_sgd_visualizer(projection, view)

    # ==========================================
    # SCENE BUILDER MODE
    # ==========================================
    def _init_scene_builder(self):
        self.grid_model = GridFloorModel(
            render_mode="Flat",
            size=500.0, spacing=1.0,
            show_x=self.state.show_grid_x,
            show_y=self.state.show_grid_y,
            show_z=self.state.show_grid_z
        ).setup()
        
        self.light_marker = build_shape(
            "Sphere1", render_mode="Flat",
            radius=0.1, sectors=16, stacks=16,
            color=(1.0, 1.0, 0.5)
        )

    def _update_scene_builder(self):
        if self.state.grid_need_rebuild:
            self.grid_model = GridFloorModel(
                render_mode="Flat", size=500.0, spacing=1.0,
                show_x=self.state.show_grid_x, show_y=self.state.show_grid_y, show_z=self.state.show_grid_z
            ).setup()
            self.state.grid_need_rebuild = False
            
        for obj in self.state.scene_objects:
            if obj["need_rebuild"]:
                params = obj["state"].get_params_values()
                try:
                    obj["model"] = build_shape(obj["type"], **params)
                except Exception as e:
                    print(f"Error building {obj['type']}: {e}")
                    obj["model"] = None
                obj["need_rebuild"] = False

    def _draw_scene_builder(self, projection, view):
        if hasattr(self, 'grid_model') and self.grid_model is not None:
            model_matrix_grid = np.eye(4, dtype=np.float32)
            self.grid_model.draw(projection, view, model_matrix_grid)
            
        for obj in self.state.scene_objects:
            if obj["model"] is not None:
                tf = obj["state"].get_transform_values()
                T  = create_translation_matrix(tf['pos_x'], tf['pos_y'], tf['pos_z'])
                Rx = create_rotation_matrix_x(tf['rot_x'])
                Ry = create_rotation_matrix_y(tf['rot_y'])
                Rz = create_rotation_matrix_z(tf['rot_z'])
                
                model_matrix = T @ Ry @ Rx @ Rz
                
                if obj["state"].is_wireframe:
                    GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
                else:
                    GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
                
                obj["model"].draw(projection, view, model_matrix, lights=self.state.lights)
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
                
        for light in self.state.lights:
            if getattr(light, 'enabled', True):
                Lx, Ly, Lz = light.position
                T_light = create_translation_matrix(Lx, Ly, Lz)
                if hasattr(self, 'light_marker') and self.light_marker is not None:
                    self.light_marker.draw(projection, view, T_light)

    # ==========================================
    # SGD VISUALIZER MODE
    # ==========================================
    def _init_sgd_visualizer(self):
        self.sgd_surface_model = None

    def _update_sgd_visualizer(self):
        if self.state.sgd_surface_need_rebuild:
            func_data = self.state.sgd_functions[self.state.sgd_selected_func_idx]
            
            self.sgd_surface_model = FunctionGraphModel(
                func_str=func_data["formula"],
                min_x=func_data["min_x"],
                max_x=func_data["max_x"],
                min_y=func_data["min_y"],
                max_y=func_data["max_y"],
                delta_x=func_data["delta"],
                delta_y=func_data["delta"],
                render_mode="ColorInterp" # Sử dụng chế độ bản đồ nhiệt độ cao (Heatmap)
            )
            # Không quên gọi setup() để đẩy data xuống GPU
            self.sgd_surface_model.setup() 
            
            self.state.sgd_surface_need_rebuild = False

        # 2. Logic cập nhật thuật toán SGD khi đang Play
        if self.state.sgd_is_playing:
            # TODO: Tính toán Gradient và di chuyển tọa độ viên bi ở bước tiếp theo
            pass

    def _draw_sgd_visualizer(self, projection, view):
        # Thiết lập ma trận biến đổi mặc định nằm ở gốc tọa độ
        model_matrix = np.eye(4, dtype=np.float32)
        
        # Cấu hình render polygon hai mặt (để nhìn được cả từ dưới lên)
        GL.glDisable(GL.GL_CULL_FACE)
        
        # Vẽ mặt phẳng đồ thị
        if hasattr(self, 'sgd_surface_model') and self.sgd_surface_model is not None:
            self.sgd_surface_model.draw(projection, view, model_matrix)
            
        GL.glEnable(GL.GL_CULL_FACE)
        
        # TODO: Vẽ viên bi (tham số hiện tại) tại vị trí (x, y, z)