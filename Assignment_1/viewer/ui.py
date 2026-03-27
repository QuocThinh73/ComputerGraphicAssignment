import imgui


class ViewerUI:
    def __init__(self, state):
        self.state = state

    def draw(self):
        imgui.begin("Shapes")

        changed, new_shape_index = imgui.combo(
            "Select Shape",
            self.state.shape_index,
            self.state.shape_names
        )

        if changed:
            self.state.shape_index = new_shape_index
            self.state.need_rebuild_model = True
            
        current_shape = self.state.current_state
        
        imgui.separator()
        imgui.text(f"{current_shape.name} Parameters")
        
        for param_id, param in current_shape.params.items():
            changed_p, new_val = imgui.slider_float(
                param.label,
                param.value,
                param.min_val,
                param.max_val
            )
            if changed_p:
                param.value = new_val
                self.state.need_rebuild_model = True

        imgui.end()