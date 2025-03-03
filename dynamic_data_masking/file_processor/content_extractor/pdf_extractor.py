import pdfplumber

from dynamic_data_masking.file_processor.content_extractor import ContentExtractor
from dynamic_data_masking.file_processor.image_processor import ImageTextProcessor, ImageCoordinateProcessor, PageToImageConverter

class PDFProcessor(ContentExtractor):
    """Handles PDF processing, extracting text and word coordinates."""

    def __init__(self, file_path, language, resolution, ocr_config):
        super().__init__(file_path, language, resolution, ocr_config)
        self.text_processor = ImageTextProcessor()
        self.coord_processor = ImageCoordinateProcessor()

    def process(self):
        """Processes a PDF and extracts text along with word coordinates."""
        extracted_text = ""
        all_word_data = []

        with pdfplumber.open(self.file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                image = PageToImageConverter.convert(page, resolution=self.resolution)

                # Extract Text
                page_text = self.text_processor.process(image, lang=self.language, ocr_config=self.ocr_config)
                extracted_text += page_text

                # Extract Word Coordinates
                word_data = self.coord_processor.process(image, page, page_num, lang=self.language)
                all_word_data.extend(word_data)

        return extracted_text, all_word_data