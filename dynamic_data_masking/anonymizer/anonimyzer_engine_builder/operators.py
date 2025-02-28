from presidio_anonymizer.entities import OperatorConfig

class OperatorConfigBuilder:
    def __init__(self, operator_name):
        self.operator_name = operator_name
        self.params = {}

    def with_param(self, key, value):
        """Adds a parameter to the operator."""
        self.params[key] = value
        return self

    def build(self):
        """Builds and returns an OperatorConfig object."""
        return OperatorConfig(self.operator_name, self.params)
