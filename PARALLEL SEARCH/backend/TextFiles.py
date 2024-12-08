from flask import Flask, request, jsonify
from concurrent.futures import ProcessPoolExecutor
import os, re

def process_chunk(chunk, start_line, pattern, fileName):
    matches = []
    regex = re.compile(pattern, re.IGNORECASE)  # Compile the regex pattern once
    print(f"Process {os.getpid()} starting to process file '{fileName}' from line {start_line}")
    
    for i, line in enumerate(chunk):
        if regex.search(line):
            matches.append({
                "lineNumber": start_line + i,
                "line": line.strip(),
                "processId": os.getpid(),
                "fileName": fileName
            })
            print(f"Process {os.getpid()} found pattern in file '{fileName}', line {start_line + i}")
    
    print(f"Process {os.getpid()} finished processing file '{fileName}' up to line {start_line + len(chunk)}")
    return matches

def divide_into_chunks(lines, chunk_size):
    for i in range(0, len(lines), chunk_size):
        yield lines[i:i + chunk_size]

def parallel_search_in_file_content(file_content, pattern, fileName):
    try:
        lines = file_content.splitlines()
        total_lines = len(lines)
        total_cores = os.cpu_count()
        chunk_size = total_lines // total_cores

        if total_lines % total_cores != 0:
            chunk_size += 1

        results = []
        with ProcessPoolExecutor() as executor:
            futures = []
            start_line = 1

            for chunk in divide_into_chunks(lines, chunk_size):
                futures.append(executor.submit(process_chunk, chunk, start_line, pattern, fileName))
                start_line += len(chunk)

            for future in futures:
                results.extend(future.result())

        return results

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def parallel_search_in_multiple_files(file_contents, pattern):
    try:
        results = []
        with ProcessPoolExecutor() as executor:
            futures = [
                executor.submit(
                    parallel_search_in_file_content,
                    file_content['content'],
                    pattern,
                    file_content['filename']
                ) for file_content in file_contents
            ]

            for future, file_content in zip(futures, file_contents):
                matches = future.result()
                if matches:
                    results.append({
                        "fileName": file_content['filename'],
                        "matches": matches
                    })

        return results

    except Exception as e:
        print(f"An error occurred in multiple file search: {e}")
        return []

def text_files_searching():
    try:
        pattern = request.form.get("pattern")
        uploaded_files = request.files.getlist("files")

        if not pattern:
            return jsonify({"error": "No search pattern provided"}), 400
        
        if not uploaded_files:
            return jsonify({"error": "No files uploaded"}), 400

        file_contents = []
        for uploaded_file in uploaded_files:
            file_contents.append({
                "filename": uploaded_file.filename,
                "content": uploaded_file.read().decode('utf-8')
            })

        results = parallel_search_in_multiple_files(file_contents, pattern)
        return jsonify(results)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal error occurred"}), 500
