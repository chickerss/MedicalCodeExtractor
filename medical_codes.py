import re

# Regular expression patterns for medical codes
CPT_PATTERN = r'(?<!\d)\d{5}(?!\d)'  # 5-digit codes
HCPCS_PATTERN = r'[A-Z]\d{4}'  # Letter followed by 4 digits
PLA_PATTERN = r'\d{4}[A-Z]'    # 4 digits followed by a letter

def extract_cpt_codes(text):
    """Extract CPT codes from text."""
    return set(re.findall(CPT_PATTERN, text))

def extract_hcpcs_codes(text):
    """Extract HCPCS codes from text."""
    return set(re.findall(HCPCS_PATTERN, text))

def extract_pla_codes(text):
    """Extract PLA codes from text."""
    return set(re.findall(PLA_PATTERN, text))

def extract_all_codes(text):
    """Extract all types of medical codes from text."""
    return {
        'CPT': list(extract_cpt_codes(text)),
        'HCPCS': list(extract_hcpcs_codes(text)),
        'PLA': list(extract_pla_codes(text))
    }
