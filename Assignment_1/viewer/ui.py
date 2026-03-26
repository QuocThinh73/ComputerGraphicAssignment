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
            
        if self.state.current_shape_name == "Rectangle":
            imgui.separator()
            imgui.text("Rectangle Parameters")
            
            changed_w, new_w = imgui.slider_float(
                "Width",
                self.state.rectangle_width,
                0.1,
                10.0
            )
            if changed_w:
                self.state.rectangle_width = new_w
                self.state.need_rebuild_model = True
                
            changed_h, new_h = imgui.slider_float(
                "Height",
                self.state.rectangle_height,
                0.1,
                10.0
            )
            if changed_h:
                self.state.rectangle_height = new_h
                self.state.need_rebuild_model = True

        imgui.end()