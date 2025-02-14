from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

class PresidioAnalyzerBuilder:
    def __init__(self, language):
        self.language = language
        self.nlp_configuration = None
        self.provider = None
        self.recognizer_registry = None
        self.analyzer = None

    def set_nlp_configuration(self, configuration):
        """Configures the NLP engine with a given configuration."""
        self.configuration = configuration
        provider = NlpEngineProvider(nlp_configuration=self.nlp_configuration)
        self.provider = provider.create_engine()
        return self

    def set_recognizer_registry(self, recognizer_registry):
        """Sets the recognizer registry."""
        self.recognizer_registry = recognizer_registry
        return self

    def build_analyzer(self):
        """Builds the Presidio AnalyzerEngine."""
        if not self.provider:
            raise ValueError("NLP Engine not configured. Call set_nlp_configuration() first.")
        if not self.recognizer_registry:
            raise ValueError("Recognizer Registry not set. Call set_recognizer_registry() first.")
        self.analyzer = AnalyzerEngine(
            registry=self.recognizer_registry,
            nlp_engine=self.provider,
            supported_languages=[self.language]
        )
        return self.analyzer