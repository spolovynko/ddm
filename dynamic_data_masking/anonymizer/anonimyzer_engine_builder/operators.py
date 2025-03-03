from presidio_anonymizer.entities import OperatorConfig

class OperatorConfigBuilder:
    def __init__(self, operator_name):
        self.operator_name = operator_name
        self.params = {}

    def with_param(self, key, value):
        self.params[key] = value
        return self

    def build(self):
        return OperatorConfig(self.operator_name, self.params)
