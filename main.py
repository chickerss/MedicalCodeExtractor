import streamlit as st
from utils import read_pdf, create_download_data
from medical_codes import extract_all_codes
from code_descriptions import format_code_with_description

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Medical Code Extractor",
        page_icon="🏥",
        layout="wide"
    )

    # Application title and description
    st.title("Medical Code Extractor")
    st.markdown("""
    Extract medical codes (CPT, HCPCS, and PLA) from PDF documents.
    Upload one or multiple PDF files below to begin.
    """)

    # Multiple file upload
    uploaded_files = st.file_uploader(
        "Choose PDF file(s)",
        type="pdf",
        accept_multiple_files=True,
        help="Upload one or more PDF files containing medical codes"
    )

    if uploaded_files:
        try:
            # Show processing message
            with st.spinner('Processing PDF files...'):
                all_results = []

                # Progress bar for multiple files
                progress_bar = st.progress(0)
                for idx, uploaded_file in enumerate(uploaded_files):
                    # Update progress
                    progress = (idx + 1) / len(uploaded_files)
                    progress_bar.progress(progress)

                    # Show current file being processed
                    st.text(f"Processing: {uploaded_file.name}")

                    # Extract text from PDF
                    pdf_text = read_pdf(uploaded_file)

                    # Extract codes
                    codes = extract_all_codes(pdf_text)

                    # Store results with filename
                    all_results.append({
                        'filename': uploaded_file.name,
                        'codes': codes
                    })

                # Remove progress bar after completion
                progress_bar.empty()

                # Display results for each file
                st.subheader("Extracted Codes with Descriptions")

                for result in all_results:
                    with st.expander(f"Results from {result['filename']}", expanded=True):
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.markdown("### CPT Codes")
                            if result['codes']['CPT']:
                                for code in sorted(result['codes']['CPT']):
                                    st.markdown(f"```\n{format_code_with_description(code)}\n```")
                            else:
                                st.info("No CPT codes found")

                        with col2:
                            st.markdown("### HCPCS Codes")
                            if result['codes']['HCPCS']:
                                for code in sorted(result['codes']['HCPCS']):
                                    st.markdown(f"```\n{format_code_with_description(code)}\n```")
                            else:
                                st.info("No HCPCS codes found")

                        with col3:
                            st.markdown("### PLA Codes")
                            if result['codes']['PLA']:
                                for code in sorted(result['codes']['PLA']):
                                    st.markdown(f"```\n{format_code_with_description(code)}\n```")
                            else:
                                st.info("No PLA codes found")

                # Create combined download data
                if all_results:
                    combined_codes = {
                        'CPT': [],
                        'HCPCS': [],
                        'PLA': []
                    }

                    for result in all_results:
                        for code_type in combined_codes:
                            combined_codes[code_type].extend(result['codes'][code_type])

                    # Remove duplicates while preserving order
                    for code_type in combined_codes:
                        combined_codes[code_type] = list(dict.fromkeys(combined_codes[code_type]))

                    csv_data = create_download_data(combined_codes)
                    st.download_button(
                        label="Download All Extracted Codes (CSV)",
                        data=csv_data,
                        file_name="extracted_codes.csv",
                        mime="text/csv"
                    )

                # Show summary
                total_files = len(all_results)
                total_codes = sum(
                    len(codes)
                    for result in all_results
                    for codes in result['codes'].values()
                )
                st.success(f"Successfully processed {total_files} file(s) and extracted {total_codes} unique medical codes!")

        except Exception as e:
            st.error(f"Error processing files: {str(e)}")
            st.warning("Please make sure you've uploaded valid PDF files.")

    # Add footer with instructions
    st.markdown("---")
    st.markdown("""
    ### Instructions
    1. Upload one or more PDF files containing medical codes
    2. Wait for the processing to complete
    3. View the extracted codes with their descriptions for each file
    4. Download the combined results as a CSV file if needed

    ### Supported Code Types
    - CPT (Current Procedural Terminology) - 5 digit codes
    - HCPCS (Healthcare Common Procedure Coding System) - Letter followed by 4 digits
    - PLA (Proprietary Laboratory Analyses) - 4 digits followed by a letter
    """)

if __name__ == "__main__":
    main()