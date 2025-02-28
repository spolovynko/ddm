from dynamic_data_masking.anonymizer.anonymizer_engine_director import AnonymizerEngineDirector

class DynamicDataMaskingAnonimyzer:
    
    def __init__(self):
        self.anonimyzer = None
        self.operators = None

    def anonimyze(self,text, analyzer_results, use_default_operators):
        self.anonimyzer, self.operators = AnonymizerEngineDirector.build_anonymizer(use_default_operators=use_default_operators)
        anonymizer_results = self.anonimyzer.anonymize(text=text,analyzer_results=analyzer_results)
        return anonymizer_results.text
