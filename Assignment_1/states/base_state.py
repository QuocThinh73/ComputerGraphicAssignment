class Parameter:
    def __init__(self, label, value, min_val, max_val):
        self.label = label
        self.value = value
        self.min_val = min_val
        self.max_val = max_val


class FloatParam(Parameter):
    def __init__(self, label, value, min_val=0.1, max_val=10.0):
        super().__init__(label, float(value), float(min_val), float(max_val))


class IntParam(Parameter):
    def __init__(self, label, value, min_val=1, max_val=100):
        super().__init__(label, int(value), int(min_val), int(max_val))
        

class StringParam(Parameter):
    def __init__(self, label, value):
        super().__init__(label, str(value), None, None)


class BaseState:
    def __init__(self, name):
        self.name = name
        self.params = {}

    def get_params_values(self):
        return {key: param.value for key, param in self.params.items()}