# analyzer_engine_builder.py
from abc import ABC

from presidio_analyzer import AnalyzerEngine, AnalyzerEngineProvider
from presidio_analyzer.nlp_engine import NlpEngineProvider
import os
from dotenv import load_dotenv

class ConfigReader:
    _instance = None

    def __new__(cls, env_path=None):
        if cls._instance is None:
            cls._instance = super(ConfigReader, cls).__new__(cls)
            cls._instance._load_env(env_path)
        return cls._instance

    def _load_env(self, env_path):
        load_dotenv(env_path)

    def get(self, key, default=None):
        return os.getenv(key, default)

config = ConfigReader()
print(config.get('ANALYZER_CONFIG_C4'))
print(config.get('ANALYZER_CONFIG_C3'))
# from config_reader import config
NLP_CONFIGURATIONS = {
    "en": {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
    },
    "fr": {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "fr", "model_name": "fr_core_news_sm"}],
    },
    "nl": {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "nl", "model_name": "nl_core_news_sm"}],
    },
}

RECOGNIZERS = {
    'en': {
        'deny_list': {
            "GREET": ["Hello"],
            "HERO": ["Captain America"]
        },
        'regex_list': {
            "NUMBERS": ["[0-9]{5}", "[0-9]{2}"],
            "EMAIL": [r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"]
        }
    },
    'fr': {
        'deny_list': {
            "SALUT": ["Bonjour"],
            "HEROS": ["Capitaine America"]
        },
        'regex_list': {
            "EMAIL": [r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"]
        }
    },
    'nl': {
        'deny_list': {
            "GROET": ["Hallo"],
            "HELD": ["Kapitein Amerika"]
        },
        'regex_list': {
            "EMAIL": [r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"]
        }
    }
}
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

class PresidioAnalyzerDirector:
    def __init__(self, builder):
        self.builder = builder

    def construct(self, from_config_file=False, language="en", use_predefined=False):
        print('we construct')
        if from_config_file:
            print('with config file')
            if use_predefined:
                print() 
                config_file = config.get('ANALYZER_CONFIG_C3')
            else:
                config_file = config.get('ANALYZER_CONFIG_C4')
            print(config_file)
            self.builder.set_config_file(config_file)
            return self.builder.build_analyzer()
        
        else:
            print('without config file')
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
        
class DynamicDataMaskingAnalyzer:
    
    def __init__(self, from_config_file=False, language="en", use_predefined=False, ):
        self.from_config_file = from_config_file
        self.language = language
        self.use_predefined = use_predefined
        
        if self.from_config_file:
            print('this route')
            self.builder = PresidioAnalyzerEngineProviderBuilder()
        else: 
            self.builder = PresidioAnalyzerBuilder(language=self.language)
            
        print(self.builder)
        self.director = PresidioAnalyzerDirector(self.builder)

        self.analyzer = self.director.construct(from_config_file=self.from_config_file,language=self.language, use_predefined=self.use_predefined)

    def analyze_text(self, text):
        return self.analyzer.analyze(text=text, language=self.language)
    
def analyze_text(text, from_config_file=False, language="en", use_predefined=False, ):  # Change language dynamically
    ddm_analyzer = DynamicDataMaskingAnalyzer(from_config_file=from_config_file, language=language, use_predefined=use_predefined)
    results = ddm_analyzer.analyze_text(text=text)
    return results

if __name__ == '__main__':
    ('ANALYZER RUNS')
    text = "Hello, my name is Steve Rogers, I am Captain America. My zip code is 12345 and my age is 29. I live in Washington. I have hypertension"
    result = analyze_text(text=text, from_config_file=True, language='en',use_predefined=False)
    print(result)