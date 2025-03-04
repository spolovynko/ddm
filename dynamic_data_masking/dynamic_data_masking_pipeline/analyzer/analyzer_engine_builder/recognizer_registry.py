from presidio_analyzer import Pattern, PatternRecognizer, RecognizerRegistry

class RegistryRecognizerBuilder:
    def __init__(self, language, use_predefined=False):
        self.language = language
        self.use_predefined = use_predefined
        self.recognizer_registry = RecognizerRegistry(supported_languages=[language])
        self.pattern_recognizers = []

    def add_deny_list_patterns(self, deny_list_dict):
        for entity, deny_list in deny_list_dict.items():
            pattern_recognizer = PatternRecognizer(
                supported_entity=entity, deny_list=deny_list, supported_language=self.language
            )
            self.pattern_recognizers.append(pattern_recognizer)
        return self

    def add_regex_patterns(self, regex_dict):
        for entity, regex_patterns in regex_dict.items():
            compiled_patterns = [
                Pattern(name=f"{entity}_pattern_{i}", regex=regex, score=1) 
                for i, regex in enumerate(regex_patterns)
            ]
            pattern_recognizer = PatternRecognizer(
                supported_entity=entity, patterns=compiled_patterns, supported_language=self.language
            )
            self.pattern_recognizers.append(pattern_recognizer)
        return self

    def build(self):
        if self.use_predefined:
            self.recognizer_registry.load_predefined_recognizers()

        for recognizer in self.pattern_recognizers:
            self.recognizer_registry.add_recognizer(recognizer)
        return self.recognizer_registry