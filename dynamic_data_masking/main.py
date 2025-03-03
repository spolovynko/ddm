import argparse

from dynamic_data_masking.dynamic_data_masking_pipeline import *
from dynamic_data_masking.mappers import LANG_MAP, CONF_LEVEL_MAP, ANONYMIZER

def main():
    parser = argparse.ArgumentParser(description="Arguments parser for dynamic data masking engine")
    # FILE PROCESSOR STEP ARGUMENTS
    parser.add_argument("input_file_path", help='paht to the file required masking')
    parser.add_argument("--lang", type=str, default='en', choices=['en','fr','nl'], help='language of the file')
    parser.add_argument("--resolution", type=int, default=500, help="resolution for input file reading")
    parser.add_argument("--ocr-config", type=str, default='--oem 3 --psm 6', help='provides configuration for content extraction from file using OCR (Object Character Recognition)')

    # TEXT ANALYZER STEP ARGUMENTS
    parser.add_argument("--conf_level", type=str, default='c4')
    parser.add_argument("--analyzer_engine", type=str, default='from_config_file', choices=['from_config_file', 'from_code'], help='provides the option on Analyzer Engine builder code / from config file')

    # TEXT ANONYMIZER STEP ARGUMETNS
    parser.add_argument("--anonimyzer_operator", type=str, default='yes', help='type of anonimyzer')

    # FILE REDACTOR STEP ARGUMENTS
    parser.add_argument("--output_file_path", help="path to where the masked file will be generated")
    args = parser.parse_args()

    pipeline = DynamicDataMaskingPipeline()
    pipeline.add_step(FileProcessorStep(
        file_path=args.input_file_path, 
        language=LANG_MAP[args.lang], 
        resolution=args.resolution, 
        ocr_config=args.ocr_config
        )
    )
    pipeline.add_step(AnalyzerStep(
        language=args.lang,
        use_predefined=CONF_LEVEL_MAP[args.conf_level]
        )
    )
    pipeline.add_step(AnonymizerStep(
        use_default_operators=ANONYMIZER[args.anonimyzer_operator]
        )
    )

    pipeline.add_step(RedactorStep(
        input_file_path=args.input_file_path, 
        output_pdf_path=args.output_file_path
        )
    )
    pipeline.execute_pipeline()

if __name__ == "__main__":
    main()