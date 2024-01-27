import os
import argparse
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
import fitz  # PyMuPDF

def is_scanned_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        for page in doc:
            if page.get_text().strip():
                # If there's text in the PDF, it's likely not scanned
                return False
    # If no text found, it's likely scanned
    return True

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text

def extract_text_from_scanned_pdf(pdf_path):
    text = ''
    with fitz.open(pdf_path) as doc:
        for page in doc:
            pix = page.get_pixmap()
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text += pytesseract.image_to_string(image) + '\n'
    return text

def save_text_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def process_pdf(pdf_path):
    if is_scanned_pdf(pdf_path):
        return extract_text_from_scanned_pdf(pdf_path)
    else:
        return extract_text_from_pdf(pdf_path)

def extract_text_from_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(directory, filename)
            text = process_pdf(pdf_path)
            text_file_path = os.path.splitext(pdf_path)[0] + '.txt'
            save_text_to_file(text, text_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract text from PDFs in a directory.')
    parser.add_argument('directory', type=str, help='Directory containing PDF files')
    args = parser.parse_args()

    extract_text_from_directory(args.directory)
