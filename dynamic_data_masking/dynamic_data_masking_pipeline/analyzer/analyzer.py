from dynamic_data_masking.dynamic_data_masking_pipeline.analyzer.analyzer_engine_builder import PresidioAnalyzerBuilder, PresidioAnalyzerEngineProviderBuilder
from dynamic_data_masking.dynamic_data_masking_pipeline.analyzer.analyzer_engine_director import PresidioAnalyzerDirector

class DynamicDataMaskingAnalyzer:
    
    def __init__(self, from_config_file, language, use_predefined):
        self.from_config_file = from_config_file
        self.language = language
        self.use_predefined = use_predefined
        
        if self.from_config_file:
            print('opted for yaml analyzer config')
            self.builder = PresidioAnalyzerEngineProviderBuilder()
        else: 
            print('opted for code analyzer config')
            self.builder = PresidioAnalyzerBuilder(language=self.language)

        self.director = PresidioAnalyzerDirector(self.builder)

        self.analyzer = self.director.construct(from_config_file=self.from_config_file,language=self.language, use_predefined=self.use_predefined)

    def analyze_text(self, text):
        return self.analyzer.analyze(text=text, language=self.language)
