from analyzer.analyzer_director import PresidioAnalyzerDirector
from analyzer.analyzer_engine_builder import PresidioAnalyzerBuilder, RegistryRecognizerBuilder,  nlp_config, recognizers

class DynamicDataMaskingAnalyzer: 

    def __init__(self, language):
        self.language = language
        self.nlp_configuration = None
        self.deny_list_entities = None
        self.regex_patterns = None
        self.analyzer = self._set_analyzer()

    def _set_nlp_configuration(self):
        nlp_configuration = nlp_config[self.language]
        return nlp_configuration
    
    def _set_recognizer_registry(self):
        language_specific = recognizers[self.language]
        self.deny_list_entities = language_specific['deny_list']
        self.regex_patterns = language_specific['regex_list']
        recognizer_builder = RegistryRecognizerBuilder(self.language)
        recognizer_registry = (
            recognizer_builder
            .add_deny_list_patterns(self.deny_list_entities)
            .add_regex_patterns(self.regex_patterns)
            .build()
        )

        return recognizer_registry

    def _set_analyzer(self):
        builder = PresidioAnalyzerBuilder(self.language)
        director = PresidioAnalyzerDirector(builder=builder)
        analyzer = director.construct(
            nlp_configuration=self._set_nlp_configuration(),
            recognizer_registry=self._set_recognizer_registry()
        )

        return analyzer
    
    def analyze(self, text):
        analyzer_resutlt = self.analyzer.analyze(text=text, language=self.language)
        return analyzer_resutlt