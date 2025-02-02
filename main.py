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
    Upload your PDF file below to begin.
    """)

    # File upload
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload a PDF file containing medical codes"
    )

    if uploaded_file is not None:
        try:
            # Show processing message
            with st.spinner('Processing PDF...'):
                # Extract text from PDF
                pdf_text = read_pdf(uploaded_file)

                # Extract codes
                codes = extract_all_codes(pdf_text)

                # Display results in columns
                st.subheader("Extracted Codes with Descriptions")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("### CPT Codes")
                    if codes['CPT']:
                        for code in sorted(codes['CPT']):
                            st.markdown(f"```\n{format_code_with_description(code)}\n```")
                    else:
                        st.info("No CPT codes found")

                with col2:
                    st.markdown("### HCPCS Codes")
                    if codes['HCPCS']:
                        for code in sorted(codes['HCPCS']):
                            st.markdown(f"```\n{format_code_with_description(code)}\n```")
                    else:
                        st.info("No HCPCS codes found")

                with col3:
                    st.markdown("### PLA Codes")
                    if codes['PLA']:
                        for code in sorted(codes['PLA']):
                            st.markdown(f"```\n{format_code_with_description(code)}\n```")
                    else:
                        st.info("No PLA codes found")

                # Update CSV export to include descriptions
                if any(codes.values()):
                    csv_data = create_download_data(codes)
                    st.download_button(
                        label="Download Extracted Codes (CSV)",
                        data=csv_data,
                        file_name="extracted_codes.csv",
                        mime="text/csv"
                    )

                # Show summary
                total_codes = sum(len(codes_list) for codes_list in codes.values())
                st.success(f"Successfully extracted {total_codes} unique medical codes!")

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.warning("Please make sure you've uploaded a valid PDF file.")

    # Add footer with instructions
    st.markdown("---")
    st.markdown("""
    ### Instructions
    1. Upload a PDF file containing medical codes
    2. Wait for the processing to complete
    3. View the extracted codes with their descriptions
    4. Download the results as a CSV file if needed

    ### Supported Code Types
    - CPT (Current Procedural Terminology) - 5 digit codes
    - HCPCS (Healthcare Common Procedure Coding System) - Letter followed by 4 digits
    - PLA (Proprietary Laboratory Analyses) - 4 digits followed by a letter
    """)

if __name__ == "__main__":
    main()