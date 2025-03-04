import pdfplumber
from reportlab.pdfgen import canvas
from PyPDF2 import PdfWriter, PdfReader
from dynamic_data_masking.file_redactor.redactor.base_redactor import RedactionStrategy

class BlackoutRedaction(RedactionStrategy):
    def apply_redaction(self, input_pdf_path, differing_words_data, output_pdf_path):
        temp_pdf_path = "temp_overlay.pdf"

        with pdfplumber.open(input_pdf_path) as pdf:
            overlay = canvas.Canvas(temp_pdf_path)

            for page_num, page in enumerate(pdf.pages, start=1):
                page_width, page_height = page.width, page.height
                overlay.setPageSize((page_width, page_height))

                # Find words to redact on this page
                words_on_page = [word for word in differing_words_data if word['page_number'] == page_num]
                for word in words_on_page:
                    x0, y0, x1, y1 = word['start_x'], word['start_y'], word['end_x'], word['end_y']
                    overlay.setFillColor('black')
                    overlay.setStrokeColor('black')
                    overlay.setLineWidth(0.5)
                    overlay.rect(x0, page_height - y1, x1 - x0, y1 - y0, fill=1)

                overlay.showPage()
                print('black out strategy')

            overlay.save()
            print('file saved')

        input_pdf = PdfReader(input_pdf_path)
        overlay_pdf = PdfReader(temp_pdf_path)
        writer = PdfWriter()

        for i, page in enumerate(input_pdf.pages):
            if i < len(overlay_pdf.pages):
                page.merge_page(overlay_pdf.pages[i])
            writer.add_page(page)
            
        with open(output_pdf_path, "wb") as output_file:
            writer.write(output_file)