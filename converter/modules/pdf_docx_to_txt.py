import fitz  # PyMuPDF for PDF processing
from docx import Document
import os

SUPPORTED_FORMATS = {
    "input": [".pdf", ".docx"],
    "output": [".txt"]
}


def convert(input_file, output_file):
    """Convert a PDF or DOCX file to TXT."""
    input_ext = os.path.splitext(input_file)[1].lower()
    output_ext = os.path.splitext(output_file)[1].lower()

    if input_ext not in SUPPORTED_FORMATS["input"] or output_ext not in SUPPORTED_FORMATS["output"]:
        raise ValueError(f"Unsupported conversion: {input_ext} to {output_ext}")

    if input_ext == ".pdf":
        text = extract_text_from_pdf(input_file)
    elif input_ext == ".docx":
        text = extract_text_from_docx(input_file)
    else:
        raise ValueError(f"Unsupported input file format: {input_ext}")

    # Write the text to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(text)


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    pdf_document = fitz.open(file_path)
    text = []
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text.append(page.get_text("text"))
    return "\n".join(text)


def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])
