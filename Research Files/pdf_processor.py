import os
from pdf_extractor import PDFExtractor

class PDFProcessor:
    def __init__(self, directory):
        self.directory = directory

    def list_pdfs(self):
        return [os.path.join(self.directory, f) for f in os.listdir(self.directory) if f.lower().endswith('.pdf')]

    def process_pdf(self, file_path, section_title):
        extractor = PDFExtractor(file_path)
        section_text = extractor.extract_section(section_title)
        if section_text:
            return {
                'file': os.path.basename(file_path),
                'section': section_text
            }
        return None
