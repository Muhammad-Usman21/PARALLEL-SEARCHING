import fitz  # PyMuPDF
import re

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_section(self, section_title):
        document = fitz.open(self.pdf_path)
        section_text = []
        capture = False

        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text = page.get_text("text").splitlines()  # Get lines of text

            for line in text:
                normalized_line = line.strip().lower()

                # Detect section heading
                match = re.match(rf"^{section_title}\s*[:]?.*", normalized_line, re.IGNORECASE)
                if match:
                    capture = True
                    section_text.append(line.strip())  # Append the entire line
                    continue

                # Stop capturing when another heading or unrelated text style appears
                if capture and (line.isupper() or line.istitle() or re.match(r"^[0-9]+\.", line) or line.strip() == ""):
                    capture = False
                    break

                # Append to section text only if capturing
                if capture:
                    section_text.append(line.strip())

        return ' '.join(section_text).strip() if section_text else None
