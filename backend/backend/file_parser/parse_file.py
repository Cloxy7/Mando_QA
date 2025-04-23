import os
from .parse_pdf import parse_pdf
from .parse_docx import parse_docx
from .parse_txt import parse_txt
from .parse_image import parse_image

def parse_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.pdf':
        return parse_pdf(file_path)
    elif ext == '.docx':
        return parse_docx(file_path)
    elif ext in ['.jpg', '.jpeg', '.png']:
        return parse_image(file_path)
    elif ext == '.txt':
        return parse_txt(file_path)
    else:
        return "Unsupported file type"
