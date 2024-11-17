from PIL import Image

SUPPORTED_FORMATS = {
    "input": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"],
    "output": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"]
}

def convert(input_file, output_file):
    img = Image.open(input_file)
    if output_file.lower().endswith('.jpg') or output_file.lower().endswith('.jpeg'):
        img = img.convert('RGB')
    img.save(output_file)