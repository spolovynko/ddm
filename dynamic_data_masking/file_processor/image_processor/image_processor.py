from abc import ABC, abstractmethod

import pytesseract
from pytesseract import Output

class PageToImageConverter:

    @staticmethod
    def convert(page, resolution):
        return page.to_image(resolution=resolution).original

class ImageProcessor(ABC):

    @abstractmethod
    def process(self, image, lang="eng"):
        pass


class ImageTextProcessor(ImageProcessor):
    
    def process(self, image, lang="eng", ocr_config=r'--oem 3 --psm 6'):
        ocr_config = ocr_config
        return pytesseract.image_to_string(image, config=ocr_config, lang=lang)


class ImageCoordinateProcessor(ImageProcessor):
    """Processes an image to extract word coordinates and scales them to the original PDF."""

    def process(self, image, page, page_number, lang="eng"):
        ocr_data = pytesseract.image_to_data(image, output_type=Output.DICT, lang=lang)
        words_info = []

        # Scale factors to adjust OCR bounding boxes to the PDF page size
        x_scale = page.width / image.width
        y_scale = page.height / image.height

        for i in range(len(ocr_data['text'])):
            if ocr_data['text'][i].strip():  # Ignore empty text results
                word_info = {
                    'text': ocr_data['text'][i],
                    'start_x': ocr_data['left'][i] * x_scale,
                    'start_y': ocr_data['top'][i] * y_scale,
                    'end_x': (ocr_data['left'][i] + ocr_data['width'][i]) * x_scale,
                    'end_y': (ocr_data['top'][i] + ocr_data['height'][i]) * y_scale,
                    'page_number': page_number
                }
                words_info.append(word_info)

        return words_info
    

