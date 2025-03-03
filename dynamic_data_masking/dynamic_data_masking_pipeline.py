from abc import ABC, abstractmethod

from dynamic_data_masking.file_processor import DynamicDataMaskingFileProcessor
from dynamic_data_masking.analyzer import DynamicDataMaskingAnalyzer
from dynamic_data_masking.anonymizer import DynamicDataMaskingAnonimyzer
from dynamic_data_masking.file_redactor import DynamicDataMaskingFileRedactor

class PipelineStep(ABC):
    
    @abstractmethod
    def execute(self, data):
        pass

class FileProcessorStep(PipelineStep):
    def __init__(self, file_path, language, resolution, ocr_config):
        self.file_path = file_path
        self.language = language
        self.resolution = resolution
        self.ocr_config = ocr_config

    def execute(self, data=None):
        print("FILE READER RUNS")
        file_processor = DynamicDataMaskingFileProcessor(
            file_path=self.file_path, 
            language=self.language, 
            resolution=self.resolution,
            ocr_config=self.ocr_config
            )
        extracted_text, word_coordinates = file_processor.process()
        return {"text": extracted_text, "word_coordinates": word_coordinates}


class AnalyzerStep(PipelineStep):
    def __init__(self, language, use_predefined=False):
        self.language = language
        self.use_predefined = use_predefined

    def execute(self, data):
        print("ANALYZER RUNS")
        analyzer = DynamicDataMaskingAnalyzer(language=self.language, use_predefined=self.use_predefined)
        result = analyzer.analyze_text(text=data["text"])
        data["analysis_results"] = result
        return data
    
class AnonymizerStep(PipelineStep):

    def __init__(self, use_default_operators):
        self.use_default_operators = use_default_operators

    def execute(self, data):
        print("ANONYMIZER RUNS")
        anonymizer = DynamicDataMaskingAnonimyzer()
        masked_text = anonymizer.anonimyze(text=data["text"], analyzer_results=data["analysis_results"], use_default_operators=self.use_default_operators)
        data["masked_text"] = masked_text
        return data
    
class RedactorStep(PipelineStep):
    def __init__(self, input_file_path, output_pdf_path):
        self.input_file_path = input_file_path
        self.output_pdf_path = output_pdf_path

    def execute(self, data):
        print("REDACTOR RUNS")
        redactor = DynamicDataMaskingFileRedactor()
        redactor.redact_file(
            input_file_path=self.input_file_path,
            extracted_text=data["text"],
            masked_text=data["masked_text"],
            words_info=data["word_coordinates"],
            output_pdf_path=self.output_pdf_path
        )
        return data

class DynamicDataMaskingPipeline:
    def __init__(self):
        self.steps = []

    def add_step(self, step):
        self.steps.append(step)

    def execute_pipeline(self, initial_data=None):
        data = initial_data
        for step in self.steps:
            data = step.execute(data)
        return data


