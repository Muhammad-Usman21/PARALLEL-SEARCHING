from flask import request, jsonify
import concurrent.futures
import traceback
import re

def search_in_lines(lines, pattern):
    """
    Searches for the pattern in the given lines in parallel using ThreadPoolExecutor.
    The search is case-insensitive.
    """
    # Use re.IGNORECASE to make the pattern search case-insensitive
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(
            lambda item: {"line": item[1], "lineNumber": item[0] + 1}
            if re.search(pattern, item[1], re.IGNORECASE) else None,
            enumerate(lines)
        ))
    return [result for result in results if result]  # Filter out None

def process_file(file, pattern):
    """
    Reads the file, decodes it, and searches for the pattern in lines.
    """
    file_content = file.read().decode('utf-8').splitlines()
    matches = search_in_lines(file_content, pattern)
    return {"fileName": file.filename, "matches": matches}


def text_files_searching():
    try:
        # Get pattern and files from request
        pattern = request.form.get("pattern")
        uploaded_files = request.files.getlist("files")

        if not pattern or not uploaded_files:
            return jsonify({"error": "Pattern and files are required"}), 400

        results = []

        # Process files in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(process_file, file, pattern)
                for file in uploaded_files
                if file.content_type == 'text/plain'
            ]

            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        return jsonify(results), 200

    except Exception as e:
        print("Error occurred:", traceback.format_exc())
        return jsonify({"error": "Internal server error", "details": str(e)}), 500