from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

@app.route('/textFileSearch', methods=['POST'])
def text_files_searching():
    try:
        # Get the pattern from the request
        pattern = request.form.get('pattern')
        if not pattern:
            return jsonify({"error": "Pattern is required"}), 400

        # Get the uploaded files
        uploaded_files = request.files.getlist('files')
        if not uploaded_files:
            return jsonify({"error": "No files uploaded"}), 400

        results = []

        for file in uploaded_files:
            if file.content_type == 'text/plain':  # Only process text files
                file_content = file.read().decode('utf-8').splitlines()
                matches = [
                    {"line": line, "lineNumber": index + 1}
                    for index, line in enumerate(file_content)
                    if pattern in line
                ]
                results.append({"fileName": file.filename, "matches": matches})

        return jsonify(results), 200

    except Exception as e:
        print("Error occurred:", traceback.format_exc())
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
