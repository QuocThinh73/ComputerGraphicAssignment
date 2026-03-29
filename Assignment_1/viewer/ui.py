import imgui
from states.base_state import FloatParam, IntParam, StringParam, ColorParam

class ViewerUI:
    def __init__(self, state):
        self.state = state

    def draw(self):
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

        imgui.text("Add Object:")
        changed_type, new_type_idx = imgui.combo("##TypeSelect", self.state.selected_add_index, self.state.available_types)
        if changed_type:
            self.state.selected_add_index = new_type_idx

        imgui.same_line()
        if imgui.button("Add"):
            selected_type = self.state.available_types[self.state.selected_add_index]
            self.state.add_object(selected_type)

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
                    changed_shader, new_shader_idx = imgui.combo("Shader Mode", obj_state.shader_index, obj_state.shader_names)
                    if changed_shader:
                        obj_state.shader_index = new_shader_idx
                        selected_obj["need_rebuild"] = True
                        
                    changed_wf, new_wf = imgui.checkbox(f"Wireframe Mode##wf_{selected_obj['id']}", obj_state.is_wireframe)
                    if changed_wf:
                        obj_state.is_wireframe = new_wf
                        
                    imgui.separator()
                    
                    current_shader = obj_state.shader_names[obj_state.shader_index].lower()
                    
                    for param_id, param in obj_state.params.items():
                        changed_p = False
                        new_val = param.value
                        unique_label = f"{param.label}##{param_id}_{selected_obj['id']}"
                        
                        if isinstance(param, FloatParam):
                            changed_p, new_val = imgui.slider_float(unique_label, param.value, param.min_val, param.max_val)
                            
                        elif isinstance(param, IntParam):
                            changed_p, new_val = imgui.slider_int(unique_label, param.value, param.min_val, param.max_val)
                            
                        elif isinstance(param, StringParam):
                            changed_p, new_val = imgui.input_text(unique_label, param.value, 256, flags=imgui.INPUT_TEXT_ENTER_RETURNS_TRUE)
                            if changed_p:
                                param.value = new_val
                                
                            param.value = new_val 
                            
                            if changed_p:
                                selected_obj["need_rebuild"] = True
                                
                        elif isinstance(param, ColorParam) and "flat" in current_shader:
                            changed_p, new_val = imgui.color_edit3(unique_label, *param.value)

                        if changed_p:
                            param.value = new_val
                            selected_obj["need_rebuild"] = True
        else:
            imgui.text_disabled("Select an object to edit its properties.")

        imgui.end()
        
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
        
        imgui.begin("Lighting Manager")
        
        if imgui.button("Add New Light (White)"):
            self.state.add_light()
            # Kích hoạt vẽ lại scene
            for obj in self.state.scene_objects:
                obj["need_rebuild"] = True

        imgui.separator()

        for i, light in enumerate(self.state.lights):
            imgui.push_id(str(i)) # Chống trùng ID UI
            
            # Checkbox Bật/Tắt
            changed_on, new_on = imgui.checkbox(f"Light {i+1}", getattr(light, 'enabled', True))
            if changed_on:
                light.enabled = new_on
                for obj in self.state.scene_objects: obj["need_rebuild"] = True
                
            imgui.same_line()
            
            # Nút xóa đèn
            if imgui.button("Delete"):
                self.state.remove_light(i)
                for obj in self.state.scene_objects: obj["need_rebuild"] = True
                
            imgui.pop_id()
            
        imgui.end()