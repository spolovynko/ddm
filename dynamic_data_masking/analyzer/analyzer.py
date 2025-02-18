from analyzer.analyzer_engine_builder import PresidioAnalyzerBuilder, PresidioAnalyzerEngineProviderBuilder
from analyzer.analyzer_engine_director import PresidioAnalyzerDirector

class DynamicDataMaskingAnalyzer:
    
    def __init__(self, from_config_file=False, language="en", use_predefined=False, ):
        self.from_config_file = from_config_file
        self.language = language
        self.use_predefined = use_predefined
        
        if self.from_config_file:
            self.builder = PresidioAnalyzerEngineProviderBuilder()
        else: 
            self.builder = PresidioAnalyzerBuilder(language=self.language)

        self.director = PresidioAnalyzerDirector(self.builder)

        self.analyzer = self.director.construct(from_config_file=self.from_config_file,language=self.language, use_predefined=self.use_predefined)

    def analyze_text(self, text):
        return self.analyzer.analyze(text=text, language=self.language)
