from dynamic_data_masking.dynamic_data_masking_pipeline.analyzer.analyzer_engine_builder.recognizer_registry import RegistryRecognizerBuilder
from dynamic_data_masking.dynamic_data_masking_pipeline.analyzer.analyzer_engine_builder.nlp_configuration import NLP_CONFIGURATIONS
from dynamic_data_masking.dynamic_data_masking_pipeline.analyzer.analyzer_engine_builder.recognizers import RECOGNIZERS

from dynamic_data_masking.ddm_config.config_reader import config


class PresidioAnalyzerDirector:
    def __init__(self, builder):
        self.builder = builder

    def construct(self, from_config_file=False, language="en", use_predefined=False):
        if from_config_file:
            if use_predefined:
                print() 
                config_file = r'dynamic_data_masking\ddm_config\analyzer_config\all-config-C3.yaml'
            else:
                config_file = r'dynamic_data_masking\ddm_config\analyzer_config\all-config-C4.yaml'

            self.builder.set_config_file(config_file)
            return self.builder.build_analyzer()
        
        else:
            if language not in NLP_CONFIGURATIONS:
                print(f"Warning: Language '{language}' not found, defaulting to English.")
                language = "en"

            configuration = NLP_CONFIGURATIONS[language]
            recognizer_data = RECOGNIZERS.get(language, {'deny_list': {}, 'regex_list': {}})

            recognizer_builder = RegistryRecognizerBuilder(language=language, use_predefined=use_predefined)
            recognizer_registry = (
                recognizer_builder
                .add_deny_list_patterns(recognizer_data['deny_list'])
                .add_regex_patterns(recognizer_data['regex_list'])
                .build()
            )

            self.builder.set_nlp_configuration(configuration)
            self.builder.set_recognizer_registry(recognizer_registry)
            return self.builder.build_analyzer()
