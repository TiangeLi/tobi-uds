from dotenv import load_dotenv
load_dotenv(override=True)

from fpdf import FPDF
import streamlit as st
from agent import chain

from langchain_text_splitters import MarkdownHeaderTextSplitter

pdf_font = "DejaVuSans.ttf"
pdf_bold_font = "DejaVuSans-Bold.ttf"
pdf_italic_font = "DejaVuSans-Oblique.ttf"
pdf_bold_italic_font = "DejaVuSans-BoldOblique.ttf"

headers_to_split_on = [
    ("#", "Title"),
    ("##", "Header 1"),
    ("###", "Header 2"),
    ("####", "Header 3"),
    ("#####", "Header 4"),
    ("######", "Header 5"),
    ("#######", "Header 6")
]

heading_font_sizes = {
    "Title": 15,
    "Header 1": 14,
    "Header 2": 13,
    "Header 3": 12,
    "Header 4": 11,
    "Header 5": 11,
    "Header 6": 10
}

markdown_splitter_with_header = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
    strip_headers=True)

def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', pdf_font, uni=True)
    pdf.add_font('DejaVu', 'b', pdf_bold_font, uni=True)  # Bold font
    pdf.add_font('DejaVu', 'i', pdf_italic_font, uni=True)  # Italic font
    pdf.add_font('DejaVu', 'bi', pdf_bold_italic_font, uni=True)  # Bold-Italic font
    docs = markdown_splitter_with_header.split_text(f'{text}')

    pdf.set_font("DejaVu", size=16)
    pdf.write(text="Your Urodynamics Report")
    pdf.ln()
    pdf.ln()

    for doc in docs:
        try:
            heading = doc.metadata[list(doc.metadata.keys())[-1]]
            heading_font_size = heading_font_sizes[list(doc.metadata.keys())[-1]]
        except IndexError:
            heading = ''
            heading_font_size = 10
        content = doc.page_content
        
        pdf.set_font("DejaVu", size=heading_font_size)
        pdf.write(text=heading)
        pdf.ln()
        pdf.set_font("DejaVu", size=10)
        pdf.multi_cell(w=0, txt=content, markdown=True)
        pdf.ln()

    pdf.output("report.pdf")

st.set_page_config(layout="wide", page_title='UDS Report Explainer')
st.write("#### UDS Report Explainer")
st.caption("Paste a urodynamics report to get a patient-oriented explanation.")

if "running" not in st.session_state:
    st.session_state.running = False
if "raw_report" not in st.session_state:
    st.session_state.raw_report = ""
if "formatted_report" not in st.session_state:
    st.session_state.formatted_report = ""

left_col, right_col = st.columns((1, 3))

with left_col:
    raw_report = st.text_area("Urodynamics Report", height=400)
    success = st.empty()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit"):
            st.session_state.raw_report = raw_report
            st.session_state.running = True
            st.session_state.formatted_report = ""
            st.rerun()
    with col2:
        download = st.empty()

with right_col:
    if st.session_state.running:
        with st.spinner('Generating...'):
            report_area = st.empty()
            report = chain.stream(st.session_state.raw_report)
            for chunk in report:
                st.session_state.formatted_report += chunk
                report_area.markdown(st.session_state.formatted_report)
        st.session_state.running = False
        generate_pdf(st.session_state.formatted_report)
        success.success("Report generated successfully!")
        with open("report.pdf", "rb") as f:
            download.download_button("Download PDF", f, "report.pdf")
    else:
        st.markdown(st.session_state.formatted_report)