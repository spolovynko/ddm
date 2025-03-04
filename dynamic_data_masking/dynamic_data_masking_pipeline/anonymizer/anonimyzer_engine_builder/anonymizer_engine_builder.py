from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.operators import Operator
from presidio_anonymizer.entities import OperatorConfig


class AnonymizerEngineBuilder:
    def __init__(self):
        self.operators = {}
        self.custom_operators = {}

    def add_operator(self, entity_type: str, operator_config: OperatorConfig):
        """Add an operator for a specific entity type."""
        self.operators[entity_type] = operator_config
        return self

    def add_custom_operator(self, operator_name: str, operator_class: type[Operator]):
        """Register a custom anonymization operator."""
        self.custom_operators[operator_name] = operator_class
        return self

    def build(self):
        """Build and return an AnonymizerEngine instance with optional operators."""
        anonymizer = AnonymizerEngine()
        for name, op_class in self.custom_operators.items():
            anonymizer.add_anonymizer(name, op_class)
        return anonymizer, self.operators if self.operators else None  # Operators are optional

