from pathlib import Path
import pdfplumber

from dynamic_data_masking.dynamic_data_masking_pipeline.file_processor.content_extractor.pdf_extractor import PDFProcessor

class DynamicDataMaskingFileProcessor:
    """Determines the correct processing function based on file type."""

    def __init__(self, file_path, language, resolution, ocr_config):
        self.file_path = Path(file_path)
        self.language = language
        self.resolution = resolution
        self.ocr_config = ocr_config
        self.file_extension = self.file_path.suffix.lower()

        # Mapping file types to their respective processors
        self.supported_types = {
            '.pdf': PDFProcessor
            # '.jpg': ,  # Future expansion
            # '.email': ,    # Future expansion
        }

    def process(self):
        """Determines and executes the correct processing function."""
        if self.file_extension in self.supported_types:
            processor_class = self.supported_types[self.file_extension]
            processor = processor_class(self.file_path, self.language, self.resolution, self.ocr_config)
            return processor.process()
        else:
            raise ValueError(f"Unsupported file type: {self.file_extension}")