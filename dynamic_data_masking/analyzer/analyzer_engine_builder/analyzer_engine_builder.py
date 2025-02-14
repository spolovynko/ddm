# analyzer_engine_builder.py

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

class PresidioAnalyzerBuilder:
    def __init__(self, language):
        self.language = language
        self.nlp_engine = None
        self.recognizer_registry = None

    def set_nlp_configuration(self, configuration):
        provider = NlpEngineProvider(nlp_configuration=configuration)
        self.nlp_engine = provider.create_engine()
        return self

    def set_recognizer_registry(self, recognizer_registry):
        self.recognizer_registry = recognizer_registry
        return self

    def build_analyzer(self):
        if not self.nlp_engine:
            raise ValueError("NLP Engine not configured. Call set_nlp_configuration() first.")
        if not self.recognizer_registry:
            raise ValueError("Recognizer Registry not set. Call set_recognizer_registry() first.")
        return AnalyzerEngine(
            registry=self.recognizer_registry,
            nlp_engine=self.nlp_engine,
            supported_languages=[self.language],
        )