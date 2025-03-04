# analyzer_engine_builder.py
from abc import ABC

from presidio_analyzer import AnalyzerEngine, AnalyzerEngineProvider
from presidio_analyzer.nlp_engine import NlpEngineProvider

class PresidioAnalyzer(ABC):

    def build_analyzer(self):
        raise NotImplementedError

class PresidioAnalyzerEngineProviderBuilder(PresidioAnalyzer):

    def __init__(self):
        self.presidio_config_file = None

    def set_config_file(self, path):
        self.presidio_config_file = path
        return self

    def build_analyzer(self):
        if not self.presidio_config_file:
            raise ValueError('NLP Engine not configured. Call set_config_file() first.')
        provider = AnalyzerEngineProvider(
            analyzer_engine_conf_file=self.presidio_config_file
        )
        analyzer = provider.create_engine()
        return analyzer

class PresidioAnalyzerBuilder(PresidioAnalyzer):
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