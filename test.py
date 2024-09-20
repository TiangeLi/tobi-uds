import streamlit as st
from langchain_text_splitters import MarkdownHeaderTextSplitter

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
    """Generate an example pdf file and save it to example.pdf"""
    from fpdf import FPDF

    print(str(text))

    pdf = FPDF()
    pdf.add_page()
    

    docs = markdown_splitter_with_header.split_text(f'{text}')

    for doc in docs:
        st.caption(doc)
        heading = doc.metadata[list(doc.metadata.keys())[-1]]
        heading_font_size = heading_font_sizes[list(doc.metadata.keys())[-1]]
        content = doc.page_content
        pdf.set_font("Arial", size=heading_font_size)
        pdf.write(text=heading)
        pdf.ln()
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(w=0, txt=content, markdown=True)
        pdf.ln()

    pdf.output("example.pdf")


text = st.text_area("Enter text to generate PDF")
if st.button("Generate PDF"):
    generate_pdf(text)
    st.success("Generated example.pdf!")

with open("example.pdf", "rb") as f:
    st.download_button("Download pdf", f, "example.pdf")