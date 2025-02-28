from main import analyze_text,anonymize_text, file_process
path = r'C:\Users\spolo\OneDrive\Documents\DOC\Work\TCS\Code\dynamic_data_masking\ddm\pdf_files\sample_sensitive_pdf.pdf'

if __name__ == "__main__":
    print('ANONYMIZER RUNS')
    text, word_coordinates = file_process(file_path=path, language='eng', resolution=300)
    print('ANALYZER RUNS')
    
    result = analyze_text(text=text, from_config_file=False, language='en',use_predefined=False)

    print('ANONYMIZER RUNS')
    masked_text = anonymize_text(text=text,analyzer_results=result)
    
    print(text)
    print(masked_text)
    print(word_coordinates)
    