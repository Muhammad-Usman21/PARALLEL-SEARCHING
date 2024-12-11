import os
import re
import fitz  # PyMuPDF
from dotenv import load_dotenv
from concurrent.futures import ProcessPoolExecutor, as_completed


def load_environment():
    """Load environment variables."""
    load_dotenv()
    return os.getenv('RESEARCH_PAPERS')


def list_pdfs(directory):
    """List all PDF files in the given directory."""
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith('.pdf')]


def extract_section_from_pdf(pdf_path, section_title):
    """
    Extract a specific section from a PDF file.
    Args:
        pdf_path (str): Path to the PDF file.
        section_title (str): Title of the section to extract.
    Returns:
        dict: File name and extracted section text.
    """
    document = fitz.open(pdf_path)
    section_text = []
    capture = False

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text("text").splitlines()

        for line in text:
            normalized_line = line.strip().lower()

            # Detect section heading
            if re.match(rf"^{section_title}\s*[:]?.*", normalized_line, re.IGNORECASE):
                capture = True
                section_text.append(line.strip())
                continue

            # Stop capturing on encountering another heading or unrelated styles
            if capture and (line.isupper() or line.istitle() or re.match(r"^[0-9]+\.", line) or line.strip() == ""):
                capture = False
                break

            if capture:
                section_text.append(line.strip())

    document.close()
    return {
        'file': os.path.basename(pdf_path),
        'section': ' '.join(section_text).strip()
    } if section_text else None


def process_file(args):
    """Process a single PDF file for a specific section."""
    pdf_path, section_title = args
    return extract_section_from_pdf(pdf_path, section_title)


def main(section_title):
    """Main function to extract sections from multiple PDFs using multiprocessing."""
    pdf_directory = load_environment()
    if not pdf_directory:
        raise ValueError("The 'RESEARCH_PAPERS' environment variable is not set.")

    pdf_files = list_pdfs(pdf_directory)
    results = []

    # Use ProcessPoolExecutor for multiprocessing
    with ProcessPoolExecutor() as executor:
        future_to_file = {executor.submit(process_file, (pdf_file, section_title)): pdf_file for pdf_file in pdf_files}
        for future in as_completed(future_to_file):
            result = future.result()
            if result:
                results.append(result)

    return results


if __name__ == '__main__':
    section_title = input("Enter the section title to extract: ")
    extracted_sections = main(section_title)
    for item in extracted_sections:
        print(f"File: {item['file']}\nSection:\n{item['section']}\n{'-'*40}\n")
