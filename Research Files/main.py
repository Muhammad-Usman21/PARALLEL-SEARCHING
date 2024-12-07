import os
import multiprocessing as mp
from dotenv import load_dotenv
from pdf_processor import PDFProcessor
from worker import Worker

def main(section_title):
    load_dotenv()
    pdf_directory = os.getenv('RESEARCH_PAPERS')
    pdf_processor = PDFProcessor(pdf_directory)
    pdf_files = pdf_processor.list_pdfs()

    file_queue = mp.JoinableQueue()
    result_queue = mp.Queue()
    num_workers = mp.cpu_count()

    # Start worker processes
    workers = []
    for _ in range(num_workers):
        worker_instance = Worker(file_queue, result_queue, section_title, pdf_processor)
        p = mp.Process(target=worker_instance.work)
        p.start()
        workers.append(p)

    # Enqueue PDF files
    for pdf_file in pdf_files:
        file_queue.put(pdf_file)

    # Add sentinel values to stop the workers
    for _ in range(num_workers):
        file_queue.put(None)

    # Wait for all files to be processed
    file_queue.join()

    # Collect results
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    # Terminate worker processes
    for p in workers:
        p.join()

    return results

if __name__ == '__main__':
    section_title = input("Enter the section title to extract: ")
    extracted_sections = main(section_title)
    for item in extracted_sections:
        print(f"File: {item['file']}\nSection:\n{item['section']}\n{'-'*40}\n")
