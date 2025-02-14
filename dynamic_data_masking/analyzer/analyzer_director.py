class PresidioAnalyzerDirector:
    def __init__(self, builder):
        self.builder = builder

    def construct(self, *args, **kwargs):
        """Adapts to different builder configurations by dynamically calling methods based on input."""
        if hasattr(self.builder, 'set_nlp_configuration') and 'configuration' in kwargs:
            self.builder.set_nlp_configuration(kwargs['configuration'])
        if hasattr(self.builder, 'set_recognizer_registry') and 'recognizer_registry' in kwargs:
            self.builder.set_recognizer_registry(kwargs['recognizer_registry'])
        if hasattr(self.builder, 'build_analyzer'):
            return self.builder.build_analyzer()
        raise ValueError("Invalid builder configuration")
