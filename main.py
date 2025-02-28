from dynamic_data_masking.config_reader import config
from dynamic_data_masking.analyzer import DynamicDataMaskingAnalyzer
from dynamic_data_masking.anonymizer import DynamicDataMaskingAnonimyzer
from dynamic_data_masking.file_processor import DynamicDataMaskingFileProcessor
from dynamic_data_masking.file_redactor import DynamicDataMaskingFileRedactor

def file_process(file_path, language='eng', resolution=500):
    file_processor = DynamicDataMaskingFileProcessor(file_path=file_path, language=language, resolution=resolution)
    extracted_text, word_coordinates = file_processor.process()
    return extracted_text, word_coordinates

def analyze_text(text, from_config_file=False, language="en", use_predefined=False, ):  # Change language dynamically
    ddm_analyzer = DynamicDataMaskingAnalyzer(from_config_file=from_config_file, language=language, use_predefined=use_predefined)
    results = ddm_analyzer.analyze_text(text=text)
    return results

def anonymize_text(text, analyzer_results,use_default_operators=False):
    anonymizer = DynamicDataMaskingAnonimyzer()
    anonymizer_text = anonymizer.anonimyze(text=text,analyzer_results=analyzer_results, use_default_operators=use_default_operators)
    return anonymizer_text

def mask_file(input_file_path, extracted_text, masked_text, words_info, output_pdf_path):
    redactor = DynamicDataMaskingFileRedactor()
    redactor.redact_file(input_file_path, extracted_text, masked_text, words_info, output_pdf_path)

