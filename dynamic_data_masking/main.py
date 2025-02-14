from config_reader import config
from analyzer import DynamicDataMaskingAnalyzer

def extract_text():
    pass

def analyze_text(text, language): 
    ddm_analyzer = DynamicDataMaskingAnalyzer(language=language)
    analyzer_results = ddm_analyzer.analyze(text=text)
    return analyzer_results

def anonymize_text():
    pass

if __name__ == '__main__':
    ('ANALYZER RUNS')
    text = "Hello, my name is Steve Rogers, I am Captain America. My zip code is 12345 and my age is 29. I live in Washington"
    analyze_text(text=text, language='en')