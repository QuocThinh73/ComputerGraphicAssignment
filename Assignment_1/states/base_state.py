class Parameter:
    def __init__(self, label, value, min_val=0.1, max_val=10.0):
        self.label = label
        self.value = value
        self.min_val = min_val
        self.max_val = max_val

class ObjectState:
    def __init__(self, name):
        self.name = name
        self.params = {}

    def get_params_values(self):
        return {key: param.value for key, param in self.params.items()}