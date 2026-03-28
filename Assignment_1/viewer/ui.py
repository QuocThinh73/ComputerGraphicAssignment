import imgui
from states.base_state import FloatParam, IntParam, StringParam

class ViewerUI:
    def __init__(self, state):
        self.state = state

    def draw(self):
        imgui.begin("Scene Manager")

        changed_shader, new_shader_idx = imgui.combo("Shader", self.state.shader_index, self.state.shader_names)
        if changed_shader:
            self.state.shader_index = new_shader_idx
            for obj in self.state.scene_objects:
                obj["need_rebuild"] = True

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
                imgui.text(f"Properties: {selected_obj['name']}")
                obj_state = selected_obj["state"]
                
                for param_id, param in obj_state.params.items():
                    changed_p = False
                    new_val = param.value
                    unique_label = f"{param.label}##{param_id}_{selected_obj['id']}"
                    
                    if isinstance(param, FloatParam):
                        changed_p, new_val = imgui.slider_float(unique_label, param.value, param.min_val, param.max_val)
                    elif isinstance(param, IntParam):
                        changed_p, new_val = imgui.slider_int(unique_label, param.value, param.min_val, param.max_val)
                    elif isinstance(param, StringParam):
                        changed_p, new_val = imgui.input_text(unique_label, param.value, 256)

                    if changed_p:
                        param.value = new_val
                        selected_obj["need_rebuild"] = True
        else:
            imgui.text_disabled("Select an object to edit its properties.")

        imgui.end()