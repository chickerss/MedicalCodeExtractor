import PyPDF2
import pandas as pd
import io

def read_pdf(pdf_file):
    """
    Extract text from a PDF file.
    
    Args:
        pdf_file: StreamletUploadedFile object
    Returns:
        str: Extracted text from PDF
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        total_pages = len(pdf_reader.pages)
        
        for page in range(total_pages):
            text += pdf_reader.pages[page].extract_text()
            
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def create_download_data(codes):
    """
    Create a downloadable CSV from extracted codes.
    
    Args:
        codes: Dictionary of extracted codes
    Returns:
        BytesIO object containing CSV data
    """
    # Create DataFrame from codes
    data = []
    for code_type, code_list in codes.items():
        for code in code_list:
            data.append({'Code Type': code_type, 'Code': code})
    
    df = pd.DataFrame(data)
    
    # Convert to CSV
    output = io.BytesIO()
    df.to_csv(output, index=False)
    return output.getvalue()
