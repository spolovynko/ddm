from dynamic_data_masking.dynamic_data_masking_pipeline.file_redactor.redactor import RedactionStrategyFactory
from dynamic_data_masking.dynamic_data_masking_pipeline.file_redactor.token_filter.word_data_mapper import WordDataMapper
from dynamic_data_masking.dynamic_data_masking_pipeline.file_redactor.token_filter.comparison import DefaultComparisonStrategy, WordDifferenceFinder

class DynamicDataMaskingFileRedactor:
    def __init__(self, comparison_strategy=None, redaction_strategy="blackout"):
        self.comparison_strategy = comparison_strategy or DefaultComparisonStrategy()
        self.redaction_strategy = RedactionStrategyFactory.get_redaction_strategy(redaction_strategy)

    def redact_file(self, input_file_path, extracted_text, masked_text, words_info, output_pdf_path):
        # Step 1: Identify differing words
        difference_finder = WordDifferenceFinder(self.comparison_strategy)
        differing_words = difference_finder.find_differing_words(extracted_text, masked_text)

        # Step 2: Map words to coordinates
        data_mapper = WordDataMapper(words_info)
        differing_words_data = data_mapper.get_word_coordinates(differing_words)

        # Step 3: Apply redaction strategy
        self.redaction_strategy.apply_redaction(input_file_path, differing_words_data, output_pdf_path)
        