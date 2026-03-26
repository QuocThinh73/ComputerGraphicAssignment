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

        imgui.text(f"Current Shape: {self.state.current_shape_name}")
        imgui.text(f"Shader: {self.state.shader_name}")

        imgui.end()