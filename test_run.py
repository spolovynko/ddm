from dynamic_data_masking.dynamic_data_masking_pipeline.dynamic_data_masking_pipeline import analyze_text,anonymize_text, file_process, mask_file
path = r'C:\Users\spolo\OneDrive\Documents\DOC\Work\TCS\Code\dynamic_data_masking\ddm\pdf_files\sample_sensitive_pdf.pdf'
output_path = r'C:\Users\spolo\OneDrive\Documents\DOC\Work\TCS\Code\dynamic_data_masking\ddm\pdf_files\sample_sensitive_pdf_redacted.pdf'

if __name__ == "__main__":
    print('FILE READER RUNS')
    text, word_coordinates = file_process(
        file_path=path, 
        language='eng', 
        resolution=500
        )

    print('ANALYZER RUNS')    
    result = analyze_text(
        text=text, 
        from_config_file=False, 
        language='en', 
        use_predefined=False
        )

    print('ANONYMIZER RUNS')
    masked_text = anonymize_text(
        text=text, 
        analyzer_results=result
        )
    
    print("REDACTOR RUNS")
    mask_file(
        input_file_path=path, 
        extracted_text=text,
        masked_text=masked_text,
        words_info=word_coordinates,
        output_pdf_path=output_path
          )


    