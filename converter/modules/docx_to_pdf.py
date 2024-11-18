from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import os
from PIL import Image

SUPPORTED_FORMATS = {
    "input": [".docx"],
    "output": [".pdf"]
}


def convert(input_file, output_file):
    """Convert a DOCX file to PDF."""
    if not input_file.endswith(".docx") or not output_file.endswith(".pdf"):
        raise ValueError("Input must be a .docx file and output must be a .pdf file")

    doc = Document(input_file)
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter
    y = height - 72  # Start 1 inch from the top

    for paragraph in doc.paragraphs:
        text = paragraph.text
        if text.strip():
            c.drawString(72, y, text)  # 1 inch from the left margin
            y -= 12  # Move down for the next line
            if y < 72:  # Start a new page if out of space
                c.showPage()
                y = height - 72

    # Extract and add images while maintaining aspect ratio
    images = extract_images_from_docx(doc)
    for image_path in images:
        try:
            # Get the original image dimensions
            with Image.open(image_path) as img:
                img_width, img_height = img.size

            # Calculate new dimensions while maintaining aspect ratio
            max_width = 300
            max_height = 200
            aspect_ratio = img_width / img_height
            if img_width > max_width or img_height > max_height:
                if aspect_ratio > 1:  # Wider than tall
                    img_width = max_width
                    img_height = max_width / aspect_ratio
                else:  # Taller than wide
                    img_height = max_height
                    img_width = max_height * aspect_ratio

            # Draw the image on the PDF
            img_reader = ImageReader(image_path)
            c.drawImage(img_reader, 72, y - img_height - 10, width=img_width, height=img_height)
            y -= img_height + 20  # Move down after placing the image
            if y < 72:  # Start a new page if out of space
                c.showPage()
                y = height - 72
        finally:
            os.remove(image_path)  # Clean up temporary image files

    c.save()


def extract_images_from_docx(doc):
    """Extract images from a DOCX file and save them as temporary files."""
    images = []
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            image_data = rel.target_part.blob
            image_filename = f"temp_image_{len(images)}.png"
            with open(image_filename, "wb") as img_file:
                img_file.write(image_data)
            images.append(image_filename)
    return images
