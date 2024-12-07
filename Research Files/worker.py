import multiprocessing as mp
from pdf_processor import PDFProcessor

class Worker:
    def __init__(self, file_queue, result_queue, section_title, pdf_processor):
        self.file_queue = file_queue
        self.result_queue = result_queue
        self.section_title = section_title
        self.pdf_processor = pdf_processor

    def work(self):
        while True:
            file_path = self.file_queue.get()
            try:
                if file_path is None:
                    break
                result = self.pdf_processor.process_pdf(file_path, self.section_title)
                if result:
                    self.result_queue.put(result)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
            finally:
                self.file_queue.task_done()
