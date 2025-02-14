from presidio_analyzer import Pattern, PatternRecognizer, RecognizerRegistry

class RegistryRecognizerBuilder:
    def __init__(self, language, use_predefined=False):
        self.language = language
        self.recognizer_registry = RecognizerRegistry(supported_languages=[language])
        self.pattern_recognizers = []
        if use_predefined:
            self.recognizer_registry.load_predefined_recognizers()

    def add_deny_list_patterns(self, deny_list_entities):
        """Creates multiple deny list pattern recognizers, each with its own entity for the given language."""
        for entity, deny_list in deny_list_entities.items():
            pattern_recognizer = PatternRecognizer(
                supported_entity=entity,
                deny_list=deny_list,
                supported_language=self.language
            )
            self.pattern_recognizers.append(pattern_recognizer)
        return self

    def add_regex_patterns(self, regex_patterns):
        """Creates multiple regex pattern recognizers for different entities in the given language."""
        for entity, patterns in regex_patterns.items():
            compiled_patterns = [Pattern(name=f"{entity}_pattern", regex=regex, score=1) for regex in patterns]
            pattern_recognizer = PatternRecognizer(
                supported_entity=entity,
                patterns=compiled_patterns,
                supported_language=self.language
            )
            self.pattern_recognizers.append(pattern_recognizer)
        return self

    def build(self):
        """Adds all created recognizers to the registry and returns it."""
        for recognizer in self.pattern_recognizers:
            self.recognizer_registry.add_recognizer(recognizer)
        return self.recognizer_registry