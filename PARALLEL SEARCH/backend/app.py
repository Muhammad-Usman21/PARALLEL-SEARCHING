from flask import Flask
from flask_cors import CORS
from TextFiles import text_files_searching  # Import route handler

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Register the route from routes.py
app.add_url_rule('/textFileSearch', view_func=text_files_searching, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)
