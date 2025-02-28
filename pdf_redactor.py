from abc import ABC, abstractmethod
from collections import defaultdict
import pdfplumber
from reportlab.pdfgen import canvas
from PyPDF2 import PdfWriter, PdfReader


class WordDifferenceFinder:
    """Identifies words that differ between original and masked text."""
    def __init__(self, comparison_strategy):
        self.comparison_strategy = comparison_strategy

    def find_differing_words(self, original_text, masked_text):
        return self.comparison_strategy.compare(original_text, masked_text)


class ComparisonStrategy(ABC):
    """Abstract Strategy for comparing original and masked text."""
    @abstractmethod
    def compare(self, original_text, masked_text):
        pass


class DefaultComparisonStrategy(ComparisonStrategy):
    """Uses set difference to find missing words (case-insensitive)."""
    def compare(self, original_text, masked_text):
        original_words = set(original_text.lower().split())
        masked_words = set(masked_text.lower().split())
        return original_words.difference(masked_words)


class WordDataMapper:
    """Maps words to their corresponding OCR coordinates."""
    def __init__(self, words_info):
        # Remove empty text entries
        filtered_words_info = [word for word in words_info if word['text'].strip()]
        self.word_data_map = self._build_word_data_map(filtered_words_info)

    def _build_word_data_map(self, words_info):
        word_data_map = defaultdict(list)
        for word_data in words_info:
            word_data_map[word_data['text'].lower()].append(word_data)
        return word_data_map

    def get_word_coordinates(self, differing_words):
        differing_words_data = [
            data for word in differing_words for data in self.word_data_map.get(word, [])
        ]
        return differing_words_data


class RedactionStrategy(ABC):
    """Abstract class for redaction strategies."""
    @abstractmethod
    def apply_redaction(self, input_pdf_path, differing_words_data, output_pdf_path):
        pass


class BlackoutRedaction(RedactionStrategy):
    """Redacts words by overlaying a black box over them."""
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
            overlay.save()

        # Merge the overlay with the original PDF
        input_pdf = PdfReader(input_pdf_path)
        overlay_pdf = PdfReader(temp_pdf_path)
        writer = PdfWriter()

        for i, page in enumerate(input_pdf.pages):
            if i < len(overlay_pdf.pages):
                page.merge_page(overlay_pdf.pages[i])
            writer.add_page(page)

        with open(output_pdf_path, "wb") as output_file:
            writer.write(output_file)

        print(f"Redacted PDF saved at {output_pdf_path}")


class RedactionStrategyFactory:
    """Factory to get different redaction strategies."""
    @staticmethod
    def get_redaction_strategy(strategy_type="blackout"):
        strategies = {
            "blackout": BlackoutRedaction()
            # Future strategies: "blur": BlurRedaction(), "replace": ReplaceTextRedaction()
        }
        return strategies.get(strategy_type, BlackoutRedaction())


class DynamicDataMaskingFileRedactor:
    """Orchestrates the entire redaction process."""
    def __init__(self, comparison_strategy=None, redaction_strategy="blackout"):
        self.comparison_strategy = comparison_strategy or DefaultComparisonStrategy()
        self.redaction_strategy = RedactionStrategyFactory.get_redaction_strategy(redaction_strategy)

    def redact_file(self, input_pdf_path, extracted_text, masked_text, words_info, output_pdf_path):
        """Performs the full redaction process."""
        # Step 1: Identify differing words
        difference_finder = WordDifferenceFinder(self.comparison_strategy)
        differing_words = difference_finder.find_differing_words(extracted_text, masked_text)

        # Step 2: Map words to coordinates
        data_mapper = WordDataMapper(words_info)
        differing_words_data = data_mapper.get_word_coordinates(differing_words)

        # Step 3: Apply redaction strategy
        self.redaction_strategy.apply_redaction(input_pdf_path, differing_words_data, output_pdf_path)


# Usage Example
if __name__ == "__main__":
    input_pdf_path = r"C:\Users\spolo\OneDrive\Documents\DOC\Work\TCS\Code\dynamic_data_masking\ddm\pdf_files\sample_sensitive_pdf.pdf"
    output_pdf_path = r"C:\Users\spolo\OneDrive\Documents\DOC\Work\TCS\Code\dynamic_data_masking\ddm\pdf_files\sample_sensitive_pdf_REDACTED.pdf"

    extracted_text = """Hello, my name is John Doe.

You can reach me at john.doe @example.com or at my phone number +1-555-123-4567.

My credit card number is 4111-1111-1111-1111 and my home address is 1234 Elm Street,
Springfield.
| have diabetes, and asthma. | vote for Democratic party and | am ecologist.

Best regards, John."""
    masked_text = """<GREET>, my name is <PERSON>.

You can reach me at john.doe @example.com or at my phone number <NRP>-123-4567.

My credit card number is <DATE_TIME> and my home address is <DATE_TIME> Elm Street,
<LOCATION>.
| have diabetes, and asthma. | vote for <NRP> party and | am ecologist.

Best regards, <PERSON>.  """

    words_info = [{'text': '',
  'start_x': 0.0,
  'start_y': 0.0,
  'end_x': 2356.0,
  'end_y': 3136.0,
  'page_number': 1},
 {'text': '',
  'start_x': 105.97824226867132,
  'start_y': 123.98273487005234,
  'end_x': 655.0204131524264,
  'end_y': 168.04628524198733,
  'page_number': 1},
 {'text': '',
  'start_x': 105.97824226867132,
  'start_y': 123.98273487005234,
  'end_x': 655.0204131524264,
  'end_y': 168.04628524198733,
  'page_number': 1},
 {'text': '',
  'start_x': 105.97824226867132,
  'start_y': 123.98273487005234,
  'end_x': 655.0204131524264,
  'end_y': 168.04628524198733,
  'page_number': 1},
 {'text': 'Hello,',
  'start_x': 105.97824226867132,
  'start_y': 123.98273487005234,
  'end_x': 209.94059405940595,
  'end_y': 164.01432638442463,
  'page_number': 1},
 {'text': 'my',
  'start_x': 227.93961618384063,
  'start_y': 134.06263201395905,
  'end_x': 282.94462779611297,
  'end_y': 168.04628524198733,
  'page_number': 1},
 {'text': 'name',
  'start_x': 297.05586114166977,
  'start_y': 135.07062172834972,
  'end_x': 402.02615817137274,
  'end_y': 160.99035724125264,
  'page_number': 1},
 {'text': 'is',
  'start_x': 418.0092898178707,
  'start_y': 127.00670401322435,
  'end_x': 446.95171739396164,
  'end_y': 160.99035724125264,
  'page_number': 1},
 {'text': 'John',
  'start_x': 460.0550055005501,
  'start_y': 128.01469372761503,
  'end_x': 552.0660066006601,
  'end_y': 161.9983469556433,
  'page_number': 1},
 {'text': 'Doe.',
  'start_x': 569.0570834861264,
  'start_y': 128.01469372761503,
  'end_x': 655.0204131524264,
  'end_y': 161.9983469556433,
  'page_number': 1},
 {'text': '',
  'start_x': 105.97824226867132,
  'start_y': 226.94168426852787,
  'end_x': 1857.9310597726442,
  'end_y': 276.0451832124162,
  'page_number': 1},
 {'text': '',
  'start_x': 105.97824226867132,
  'start_y': 226.94168426852787,
  'end_x': 1857.9310597726442,
  'end_y': 276.0451832124162,
  'page_number': 1},
 {'text': '',
  'start_x': 105.97824226867132,
  'start_y': 226.94168426852787,
  'end_x': 1857.9310597726442,
  'end_y': 276.0451832124162,
  'page_number': 1},
 {'text': 'You',
  'start_x': 105.97824226867132,
  'start_y': 226.94168426852787,
  'end_x': 179.99022124434669,
  'end_y': 261.0693360271834,
  'page_number': 1},
 {'text': 'can',
  'start_x': 194.96540765187632,
  'start_y': 237.02158141243456,
  'end_x': 261.0578168928004,
  'end_y': 261.9333272109468,
  'page_number': 1},
 {'text': 'reach',
  'start_x': 278.04889377826674,
  'start_y': 230.97364312609054,
  'end_x': 382.0112455690014,
  'end_y': 263.94930663972815,
  'page_number': 1},
 {'text': 'me',
  'start_x': 397.99437721549936,
  'start_y': 239.0375608412159,
  'end_x': 455.0152793057084,
  'end_y': 264.95729635411885,
  'page_number': 1},
 {'text': 'at',
  'start_x': 469.99046571323805,
  'start_y': 235.00560198365324,
  'end_x': 503.9726194841707,
  'end_y': 264.95729635411885,
  'page_number': 1},
 {'text': 'john.doe',
  'start_x': 520.387727661655,
  'start_y': 226.36569014601892,
  'end_x': 683.9628407285173,
  'end_y': 277.1971714574341,
  'page_number': 1},
 {'text': '@example.com',
  'start_x': 706.8575968707983,
  'start_y': 226.36569014601892,
  'end_x': 977.994866153282,
  'end_y': 277.1971714574341,
  'page_number': 1},
 {'text': 'or',
  'start_x': 1007.9452389683414,
  'start_y': 241.05354026999726,
  'end_x': 1044.951228456179,
  'end_y': 266.97327578290015,
  'page_number': 1},
 {'text': 'at',
  'start_x': 1060.0704070407041,
  'start_y': 236.01359169804388,
  'end_x': 1095.0605060506052,
  'end_y': 267.98126549729085,
  'page_number': 1},
 {'text': 'my',
  'start_x': 1111.0436376971031,
  'start_y': 242.0615299843879,
  'end_x': 1167.0565945483438,
  'end_y': 276.0451832124162,
  'page_number': 1},
 {'text': 'phone',
  'start_x': 1183.0397261948417,
  'start_y': 233.99761226926256,
  'end_x': 1306.0090453489795,
  'end_y': 276.0451832124162,
  'page_number': 1},
 {'text': 'number',
  'start_x': 1323.0001222344458,
  'start_y': 233.99761226926256,
  'end_x': 1476.0638063806382,
  'end_y': 268.9892552116815,
  'page_number': 1},
 {'text': '+1-555-123-4567.',
  'start_x': 1490.0310475491995,
  'start_y': 235.00560198365324,
  'end_x': 1857.9310597726442,
  'end_y': 268.9892552116815,
  'page_number': 1},
 {'text': '',
  'start_x': 107.994132746608,
  'start_y': 329.03664248324,
  'end_x': 2111.933259992666,
  'end_y': 383.0360914684544,
  'page_number': 1},
 {'text': '',
  'start_x': 107.994132746608,
  'start_y': 329.03664248324,
  'end_x': 2111.933259992666,
  'end_y': 383.0360914684544,
  'page_number': 1},
 {'text': '',
  'start_x': 107.994132746608,
  'start_y': 329.03664248324,
  'end_x': 2111.933259992666,
  'end_y': 383.0360914684544,
  'page_number': 1},
 {'text': 'My',
  'start_x': 107.994132746608,
  'start_y': 329.03664248324,
  'end_x': 162.99914435888036,
  'end_y': 370.94021489576636,
  'page_number': 1},
 {'text': 'credit',
  'start_x': 190.93362669600296,
  'start_y': 332.06061162641197,
  'end_x': 295.0399706637331,
  'end_y': 364.0282854256589,
  'page_number': 1},
 {'text': 'card',
  'start_x': 323.982398239824,
  'start_y': 333.0686013408026,
  'end_x': 405.04999388827775,
  'end_y': 365.0362751400496,
  'page_number': 1},
 {'text': 'number',
  'start_x': 436.0083119423054,
  'start_y': 333.9325925245661,
  'end_x': 582.0163794157194,
  'end_y': 367.0522545688309,
  'page_number': 1},
 {'text': 'is',
  'start_x': 610.9588069918103,
  'start_y': 333.9325925245661,
  'end_x': 639.0372815059284,
  'end_y': 367.0522545688309,
  'page_number': 1},
 {'text': '4111-1111-1111-1111',
  'start_x': 667.9797090820193,
  'start_y': 335.9485719533474,
  'end_x': 1099.9562400684513,
  'end_y': 370.94021489576636,
  'page_number': 1},
 {'text': 'and',
  'start_x': 1137.9701747952574,
  'start_y': 338.9725410965194,
  'end_x': 1209.966263292996,
  'end_y': 371.94820461015706,
  'page_number': 1},
 {'text': 'my',
  'start_x': 1241.932526585992,
  'start_y': 347.03645881164476,
  'end_x': 1299.9613739151694,
  'end_y': 382.02810175406375,
  'page_number': 1},
 {'text': 'home',
  'start_x': 1331.0636841461926,
  'start_y': 338.9725410965194,
  'end_x': 1442.9456056716783,
  'end_y': 372.9561943245477,
  'page_number': 1},
 {'text': 'address',
  'start_x': 1474.0479159027016,
  'start_y': 339.98053081091007,
  'end_x': 1636.0391150226135,
  'end_y': 374.97217375332906,
  'page_number': 1},
 {'text': 'is',
  'start_x': 1668.0053783156095,
  'start_y': 340.98852052530077,
  'end_x': 1698.963696369637,
  'end_y': 374.97217375332906,
  'page_number': 1},
 {'text': '1234',
  'start_x': 1731.9379049016015,
  'start_y': 340.98852052530077,
  'end_x': 1832.0124679134583,
  'end_y': 375.9801634677197,
  'page_number': 1},
 {'text': 'Elm',
  'start_x': 1864.9866764454225,
  'start_y': 341.9965102396914,
  'end_x': 1941.0145458990346,
  'end_y': 375.9801634677197,
  'page_number': 1},
 {'text': 'Street,',
  'start_x': 1976.0046449089355,
  'start_y': 340.98852052530077,
  'end_x': 2111.933259992666,
  'end_y': 383.0360914684544,
  'page_number': 1},
 {'text': '',
  'start_x': 107.994132746608,
  'start_y': 429.97961245293413,
  'end_x': 317.93472680601394,
  'end_y': 473.03517311047847,
  'page_number': 1},
 {'text': '',
  'start_x': 107.994132746608,
  'start_y': 429.97961245293413,
  'end_x': 317.93472680601394,
  'end_y': 473.03517311047847,
  'page_number': 1},
 {'text': '',
  'start_x': 107.994132746608,
  'start_y': 429.97961245293413,
  'end_x': 317.93472680601394,
  'end_y': 473.03517311047847,
  'page_number': 1},
 {'text': 'Springfield.',
  'start_x': 107.994132746608,
  'start_y': 429.97961245293413,
  'end_x': 317.93472680601394,
  'end_y': 473.03517311047847,
  'page_number': 1},
 {'text': '',
  'start_x': 107.994132746608,
  'start_y': 531.930572137019,
  'end_x': 1603.0649064906493,
  'end_y': 593.9939388373588,
  'page_number': 1},
 {'text': '',
  'start_x': 107.994132746608,
  'start_y': 531.930572137019,
  'end_x': 1603.0649064906493,
  'end_y': 593.9939388373588,
  'page_number': 1},
 {'text': '',
  'start_x': 107.994132746608,
  'start_y': 531.930572137019,
  'end_x': 1603.0649064906493,
  'end_y': 593.9939388373588,
  'page_number': 1},
 {'text': '|',
  'start_x': 107.994132746608,
  'start_y': 531.930572137019,
  'end_x': 114.04180418041805,
  'end_y': 564.0422444668932,
  'page_number': 1},
 {'text': 'have',
  'start_x': 131.03288106588437,
  'start_y': 531.930572137019,
  'end_x': 221.0279916880577,
  'end_y': 565.0502341812838,
  'page_number': 1},
 {'text': 'diabetes,',
  'start_x': 234.99523285661903,
  'start_y': 532.9385618514096,
  'end_x': 407.9298374281873,
  'end_y': 573.9781430801727,
  'page_number': 1},
 {'text': 'and',
  'start_x': 425.0649064906491,
  'start_y': 537.978510423363,
  'end_x': 496.0530497494194,
  'end_y': 570.9541739370006,
  'page_number': 1},
 {'text': 'asthma.',
  'start_x': 511.02823615694905,
  'start_y': 539.9944898521444,
  'end_x': 662.9399828871776,
  'end_y': 573.9781430801727,
  'page_number': 1},
 {'text': '|',
  'start_x': 681.9469502505807,
  'start_y': 541.002479566535,
  'end_x': 687.9946216843907,
  'end_y': 573.9781430801727,
  'page_number': 1},
 {'text': 'vote',
  'start_x': 703.9777533308887,
  'start_y': 546.0424281384884,
  'end_x': 786.0532942183108,
  'end_y': 575.994122508954,
  'page_number': 1},
 {'text': 'for',
  'start_x': 801.0284806258404,
  'start_y': 543.0184589953163,
  'end_x': 850.9937660432711,
  'end_y': 577.0021122233446,
  'page_number': 1},
 {'text': 'Democratic',
  'start_x': 866.9768976897691,
  'start_y': 543.0184589953163,
  'end_x': 1091.0287250947317,
  'end_y': 578.0101019377353,
  'page_number': 1},
 {'text': 'party',
  'start_x': 1106.0039115022614,
  'start_y': 550.9383781798144,
  'end_x': 1204.0625840361815,
  'end_y': 589.9619799797961,
  'page_number': 1},
 {'text': 'and',
  'start_x': 1220.0457156826794,
  'start_y': 549.0663972816604,
  'end_x': 1293.0497494193864,
  'end_y': 582.042060795298,
  'page_number': 1},
 {'text': '|',
  'start_x': 1311.0487715438212,
  'start_y': 549.0663972816604,
  'end_x': 1316.9524508006357,
  'end_y': 582.042060795298,
  'page_number': 1},
 {'text': 'am',
  'start_x': 1333.943527686102,
  'start_y': 556.9863164661585,
  'end_x': 1393.9882654932162,
  'end_y': 583.0500505096886,
  'page_number': 1},
 {'text': 'ecologist.',
  'start_x': 1410.9793423786825,
  'start_y': 550.9383781798144,
  'end_x': 1603.0649064906493,
  'end_y': 593.9939388373588,
  'page_number': 1},
 {'text': '',
  'start_x': 106.84219533064419,
  'start_y': 631.8655523923226,
  'end_x': 106.98618750763966,
  'end_y': 664.9852144365874,
  'page_number': 1},
 {'text': '',
  'start_x': 106.84219533064419,
  'start_y': 631.8655523923226,
  'end_x': 106.98618750763966,
  'end_y': 664.9852144365874,
  'page_number': 1},
 {'text': '',
  'start_x': 106.84219533064419,
  'start_y': 631.8655523923226,
  'end_x': 106.98618750763966,
  'end_y': 664.9852144365874,
  'page_number': 1},
 {'text': ' ',
  'start_x': 106.84219533064419,
  'start_y': 631.8655523923226,
  'end_x': 106.98618750763966,
  'end_y': 664.9852144365874,
  'page_number': 1},
 {'text': '',
  'start_x': 106.98618750763966,
  'start_y': 632.0095509229498,
  'end_x': 480.06991810292146,
  'end_y': 676.9370924786482,
  'page_number': 1},
 {'text': '',
  'start_x': 106.98618750763966,
  'start_y': 632.0095509229498,
  'end_x': 480.06991810292146,
  'end_y': 676.9370924786482,
  'page_number': 1},
 {'text': '',
  'start_x': 106.98618750763966,
  'start_y': 632.0095509229498,
  'end_x': 480.06991810292146,
  'end_y': 676.9370924786482,
  'page_number': 1},
 {'text': 'Best',
  'start_x': 106.98618750763966,
  'start_y': 632.0095509229498,
  'end_x': 190.0696736340301,
  'end_y': 665.993204150978,
  'page_number': 1},
 {'text': 'regards,',
  'start_x': 205.04486004155973,
  'start_y': 636.0415097805125,
  'end_x': 359.98044248869337,
  'end_y': 676.9370924786482,
  'page_number': 1},
 {'text': 'John.',
  'start_x': 375.9635741351913,
  'start_y': 638.0574892092937,
  'end_x': 480.06991810292146,
  'end_y': 673.0491321517127,
  'page_number': 1},
 {'text': '',
  'start_x': 0.0,
  'start_y': 199.86996051060703,
  'end_x': 2356.0,
  'end_y': 3136.0,
  'page_number': 1},
 {'text': '',
  'start_x': 0.0,
  'start_y': 199.86996051060703,
  'end_x': 2356.0,
  'end_y': 3136.0,
  'page_number': 1},
 {'text': '',
  'start_x': 0.0,
  'start_y': 199.86996051060703,
  'end_x': 2356.0,
  'end_y': 3136.0,
  'page_number': 1},
 {'text': '',
  'start_x': 0.0,
  'start_y': 199.86996051060703,
  'end_x': 2356.0,
  'end_y': 3136.0,
  'page_number': 1}]

    # Create a redactor with the default strategy (blackout)
    redactor = DynamicDataMaskingFileRedactor()

    # Perform the redaction process
    redactor.redact_file(input_pdf_path, extracted_text, masked_text, words_info, output_pdf_path)
