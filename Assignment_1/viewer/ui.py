import imgui
from states.base_state import FloatParam, IntParam, StringParam, ColorParam
import numpy as np


class ViewerUI:
    def __init__(self, state):
        self.state = state
        
    def draw(self):
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("Application Mode"):
                clicked_1, _ = imgui.menu_item("Scene Builder", selected=(self.state.current_app_mode == self.state.APP_MODE_SCENE))
                if clicked_1: 
                    self.state.current_app_mode = self.state.APP_MODE_SCENE
                    
                clicked_2, _ = imgui.menu_item("SGD Visualizer", selected=(self.state.current_app_mode == self.state.APP_MODE_SGD))
                if clicked_2: 
                    self.state.current_app_mode = self.state.APP_MODE_SGD
                    
                imgui.end_menu()
            imgui.end_main_menu_bar()

        if self.state.current_app_mode == self.state.APP_MODE_SCENE:
            self._draw_scene_builder_ui()
        elif self.state.current_app_mode == self.state.APP_MODE_SGD:
            self._draw_sgd_visualizer_ui()

    def _draw_scene_builder_ui(self):
        # ==========================================
        # 1. SCENE MANAGER
        # ==========================================
        imgui.begin("Scene Manager")
        
        if imgui.collapsing_header("Environment (Grid)", flags=imgui.TREE_NODE_DEFAULT_OPEN)[0]:
            imgui.text("Toggle Axes:")
            
            changed_x, self.state.show_grid_x = imgui.checkbox("X", self.state.show_grid_x)
            imgui.same_line()
            changed_y, self.state.show_grid_y = imgui.checkbox("Y", self.state.show_grid_y)
            imgui.same_line()
            changed_z, self.state.show_grid_z = imgui.checkbox("Z", self.state.show_grid_z)
            
            if changed_x or changed_y or changed_z:
                self.state.grid_need_rebuild = True
        
        imgui.separator()

        if imgui.button("Add New Object", width=-1):
            imgui.open_popup("AddObjectPopup")

        if imgui.begin_popup("AddObjectPopup"):
            # 2D
            if imgui.begin_menu("2D"):
                shapes_2d = ["Triangle", "Rectangle", "Trapezium", "Pentagon", "Hexagon", "Circle", "Elip", "Star", "Arrow"]
                for obj_type in shapes_2d:
                    clicked, _ = imgui.menu_item(obj_type)
                    if clicked:
                        self.state.add_object(obj_type)
                imgui.end_menu()
                
            # 3D
            if imgui.begin_menu("3D"):
                shapes_3d = ["Cube", "Cone", "TruncatedCone", "Cylinder", "Tetrahedron", "Torus", "Prism", "Sphere1", "Sphere2", "Sphere3"]
                for obj_type in shapes_3d:
                    clicked, _ = imgui.menu_item(obj_type)
                    if clicked:
                        self.state.add_object(obj_type)
                imgui.end_menu()
                
            # Function Graph
            if imgui.begin_menu("Function Graph"):
                clicked, _ = imgui.menu_item("FunctionGraph")
                if clicked:
                    self.state.add_object("FunctionGraph")
                imgui.end_menu()
                
            imgui.end_popup()

        imgui.separator()

        imgui.text("Scene Objects:")
        imgui.begin_child("Hierarchy", 0, 150, border=True)
        
        for obj in self.state.scene_objects:
            obj_id = obj["id"]
            is_selected = (self.state.selected_obj_id == obj_id)
            
            clicked, _ = imgui.selectable(f"{obj['name']}##sel_{obj_id}", is_selected)
            if clicked:
                self.state.selected_obj_id = obj_id
                
        imgui.end_child()

        if self.state.selected_obj_id is not None:
            if imgui.button("Delete Selected Object"):
                self.state.remove_object(self.state.selected_obj_id)
        
        imgui.separator()

        # ==========================================
        # 2. SELECTED OBJECT DETAILS
        # ==========================================
        if self.state.selected_obj_id is not None:
            selected_obj = next((o for o in self.state.scene_objects if o["id"] == self.state.selected_obj_id), None)
            
            if selected_obj:
                obj_state = selected_obj["state"]
                
                if imgui.collapsing_header("Transform", flags=imgui.TREE_NODE_DEFAULT_OPEN)[0]:
                    for param_id, param in obj_state.transform_params.items():
                        unique_label = f"{param.label}##{param_id}_{selected_obj['id']}"
                        changed_p, new_val = imgui.slider_float(unique_label, param.value, param.min_val, param.max_val)
                        if changed_p:
                            param.value = new_val
                
                if imgui.collapsing_header("Properties", flags=imgui.TREE_NODE_DEFAULT_OPEN)[0]:
                    
                    changed_rm, new_rm_idx = imgui.combo("Render Mode", obj_state.render_mode_idx, obj_state.render_modes)
                    if changed_rm:
                        obj_state.render_mode_idx = new_rm_idx
                        selected_obj["need_rebuild"] = True
                        
                    changed_wf, new_wf = imgui.checkbox(f"Wireframe Mode##wf_{selected_obj['id']}", obj_state.is_wireframe)
                    if changed_wf:
                        obj_state.is_wireframe = new_wf
                        
                    imgui.separator()
                    
                    current_mode = obj_state.render_modes[obj_state.render_mode_idx]
                  
                    for param_id, param in obj_state.params.items():
                        unique_label = f"{param.label}##{param_id}_{selected_obj['id']}"
                        changed_p = False
                        new_val = param.value
                        
                        if isinstance(param, FloatParam):
                            changed_p, new_val = imgui.slider_float(unique_label, param.value, param.min_val, param.max_val)
                        elif isinstance(param, IntParam):
                            changed_p, new_val = imgui.slider_int(unique_label, param.value, param.min_val, param.max_val)
                        elif isinstance(param, StringParam):
                            changed_p, new_val = imgui.input_text(unique_label, param.value, 256, flags=imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)
                        
                        if changed_p:
                            param.value = new_val
                            selected_obj["need_rebuild"] = True
                            
                    imgui.separator()
                    
                    for param_id, param in obj_state.material_params.items():
                        is_lit = current_mode in ["Phong", "Gouraud"]
                        
                        if param_id == 'color' and is_lit: continue
                        if param_id == 'color' and current_mode == "Texture": continue
                        if param_id in ['diffuse', 'specular', 'ambient', 'shininess'] and not is_lit: continue
                        if param_id == 'texture_path' and current_mode != "Texture": continue
                        
                        unique_label = f"{param.label}##{param_id}_{selected_obj['id']}"
                        changed_p = False
                        new_val = param.value
                        
                        if isinstance(param, ColorParam):
                            changed_p, new_val = imgui.color_edit3(unique_label, *param.value)
                        elif isinstance(param, FloatParam):
                            changed_p, new_val = imgui.slider_float(unique_label, param.value, param.min_val, param.max_val)
                        elif isinstance(param, StringParam):
                            changed_p, new_val = imgui.input_text(unique_label, param.value, 256, flags=imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)
                            if changed_p: param.value = new_val
                            
                        if changed_p:
                            param.value = new_val
                            selected_obj["need_rebuild"] = True
        else:
            imgui.text_disabled("Select an object to edit its properties.")

        imgui.end()
        
        # ==========================================
        # 3. CAMERA MANAGER 
        # ==========================================
        imgui.begin("Camera Manager")
        
        if imgui.button("Add New Camera"):
            self.state.add_camera()

        imgui.separator()

        imgui.text("Available Cameras:")
        imgui.begin_child("CameraList", 0, 150, border=True)
        
        for i, cam in enumerate(self.state.cameras):
            is_selected = (i == self.state.active_camera_idx)
            clicked, _ = imgui.selectable(f"Camera {i+1}##cam_{i}", is_selected)
            if clicked:
                self.state.active_camera_idx = i
                
        imgui.end_child()

        if len(self.state.cameras) > 1:
            if imgui.button("Delete Active Camera"):
                self.state.remove_camera(self.state.active_camera_idx)

        imgui.end()
        
        # ==========================================
        # 4. LIGHTING MANAGER
        # ==========================================
        imgui.begin("Lighting Manager")
        
        if imgui.button("Add New Light (White)"):
            self.state.add_light()
            for obj in self.state.scene_objects:
                obj["need_rebuild"] = True

        imgui.separator()

        light_to_delete = None

        for i, light in enumerate(self.state.lights):
            if imgui.collapsing_header(f"Light {i+1}", flags=imgui.TREE_NODE_DEFAULT_OPEN)[0]:
                imgui.push_id(f"light_group_{i}") 
                
                changed_on, new_on = imgui.checkbox("Enabled", getattr(light, 'enabled', True))
                if changed_on: light.enabled = new_on
                    
                imgui.same_line()
                
                if imgui.button("Delete Light"):
                    light_to_delete = i
                
                if getattr(light, 'enabled', True):
                    changed_pos, new_pos = imgui.drag_float3("Position", *light.position, 0.1)
                    if changed_pos: 
                        light.position = np.array(new_pos, dtype=np.float32)
                    
                    changed_diff, new_diff = imgui.color_edit3("Diffuse Color", *light.diffuse)
                    if changed_diff: 
                        light.diffuse = np.array(new_diff, dtype=np.float32)
                    
                    changed_spec, new_spec = imgui.color_edit3("Specular", *light.specular)
                    if changed_spec: 
                        light.specular = np.array(new_spec, dtype=np.float32)
                        
                    changed_amb, new_amb = imgui.color_edit3("Ambient", *light.ambient)
                    if changed_amb: 
                        light.ambient = np.array(new_amb, dtype=np.float32)

                imgui.pop_id()
                imgui.separator()

        if light_to_delete is not None:
            self.state.remove_light(light_to_delete)
            
        imgui.end()
        
    def _draw_sgd_visualizer_ui(self):
        imgui.begin("SGD Optimization Settings")
        imgui.end()