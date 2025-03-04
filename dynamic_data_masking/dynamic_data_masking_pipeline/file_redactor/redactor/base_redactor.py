from abc import ABC, abstractmethod

class RedactionStrategy(ABC):
    @abstractmethod
    def apply_redaction(self, input_pdf_path, differing_words_data, output_pdf_path):
        pass