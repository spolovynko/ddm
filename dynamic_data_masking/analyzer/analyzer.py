from analyzer.analyzer_engine_builder import PresidioAnalyzerBuilder
from analyzer.analyzer_engine_director import PresidioAnalyzerDirector

class DynamicDataMaskingAnalyzer:
    def __init__(self, language="en", use_predefined=False):
        self.language = language
        self.use_predefined = use_predefined
        self.builder = PresidioAnalyzerBuilder(language=self.language)
        self.director = PresidioAnalyzerDirector(self.builder)
        self.analyzer = self.director.construct(language=self.language, use_predefined=self.use_predefined)

    def analyze_text(self, text):
        return self.analyzer.analyze(text=text, language=self.language)
