from viewer.model_factory import build_shape


class Scene:
    def __init__(self, state):
        self.state = state
        self.model = None
        self.rebuild_model()

    def rebuild_model(self):
        current_shape_state = self.state.current_state
        
        params = current_shape_state.get_params_values()

        self.model = build_shape(
            self.state.current_shape_name,
            self.state.shader_name,
            **params
        )
        self.state.need_rebuild_model = False

    def update(self):
        if self.state.need_rebuild_model:
            self.rebuild_model()

    def draw(self, projection, view):
        if self.model is not None:
            self.model.draw(projection, view, None)