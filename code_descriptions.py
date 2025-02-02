"""Module for medical code descriptions and lookup functionality."""

# Sample code descriptions (can be expanded)
CODE_DESCRIPTIONS = {
    # CPT Code descriptions
    '99213': 'Office/outpatient visit, established patient, 20-29 minutes',
    '99214': 'Office/outpatient visit, established patient, 30-39 minutes',
    
    # HCPCS Code descriptions
    'G0008': 'Administration of influenza virus vaccine',
    'J0171': 'Injection, adrenalin, epinephrine, 0.1 mg',
    
    # PLA Code descriptions
    '0001U': 'Red blood cell antigen typing, DNA, human erythrocyte gene analysis',
    '0002U': 'Oncology colorectal screening',
}

def get_code_description(code):
    """
    Get the description for a medical code.
    
    Args:
        code (str): The medical code to look up
        
    Returns:
        str: The description of the code, or 'Description not available' if not found
    """
    return CODE_DESCRIPTIONS.get(code, 'Description not available')

def format_code_with_description(code):
    """
    Format a code with its description for display.
    
    Args:
        code (str): The medical code to format
        
    Returns:
        str: Formatted string with code and description
    """
    description = get_code_description(code)
    return f"{code}: {description}"
