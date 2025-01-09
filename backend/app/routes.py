from app.controllers.text_files import text_files_searching
from app.controllers.research_files import research_files_searching
from app.controllers.pdf_generator import generate_pdf

def register_routes(app):
    app.add_url_rule('/textFileSearch', view_func=text_files_searching, methods=['POST'])
    app.add_url_rule('/researchFileSearch', view_func=research_files_searching, methods=['POST'])
    app.add_url_rule('/generate-pdf', view_func=generate_pdf, methods=['POST'])
