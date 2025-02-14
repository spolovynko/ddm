from config_reader import config
from analyzer import DynamicDataMaskingAnalyzer

def extract_text():
    pass


def analyze_text(text, language="en", use_predefined=False):  # Change language dynamically
    ddm_analyzer = DynamicDataMaskingAnalyzer(language=language, use_predefined=use_predefined)
    results = ddm_analyzer.analyze_text(text=text)
    return results


def anonymize_text():
    pass

if __name__ == '__main__':
    ('ANALYZER RUNS')
    text = "Hello, my name is Steve Rogers, I am Captain America. My zip code is 12345 and my age is 29. I live in Washington"
    result = analyze_text(text=text, language='en',use_predefined=True)
    print(result)