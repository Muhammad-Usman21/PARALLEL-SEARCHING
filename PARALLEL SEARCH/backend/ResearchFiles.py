from flask import Flask, request, jsonify
from concurrent.futures import ProcessPoolExecutor, as_completed
import fitz  # PyMuPDF
import re
import traceback



def extract_title_from_pdf(document):
    """Title extraction based on font size and positioning in the whole document."""
    try:
        title = "Unknown Title"
        
        # Extract text with details (font size, font style, position)
        text_instances = []
        
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text_dict = page.get_text("dict")
            
            # print(f"Page {page_num} text data: {text_dict}")
            
            if "blocks" not in text_dict:
                raise ValueError(f"Missing 'blocks' in page {page_num} text data")
                
            text_instances += text_dict["blocks"]  # Get text blocks with details
        
        # Analyze text blocks for large fonts
        possible_titles = []
        
        for block in text_instances:
            if block.get("type", -1) == 0:  # Ensure it's a text block
                for line in block.get("lines", []):  # Iterate over lines
                    for span in line.get("spans", []):  # Iterate over spans
                        block_text = span.get("text", "").strip()
                        block_font_size = span.get("size", 4)  # Default to 12 if font size not found

                        if block_text and len(block_text) > 5:  # Ensure text is meaningful
                            # Perform your logic with block_text and block_font_size
                            # Ignore blocks with numbers as their main content
                            if re.search(r"\d", block_text):
                                continue  # Skip lines containing any number

                            # print(f"Text: {block_text}, Font Size: {block_font_size}")
                            possible_titles.append((block_text, block_font_size))
                            
        if possible_titles:
            # Sort by font size (largest first)
            possible_titles.sort(key=lambda x: x[1], reverse=True)
            
            # Find the largest font size
            largest_font_size = possible_titles[0][1]

            # Filter out titles with the largest font size, and exclude lines that are numeric-only
            largest_titles = [
                title[0]
                for title in possible_titles
                if title[1] == largest_font_size
            ]

            # If no valid titles found, fallback to "Unknown Title"
            if largest_titles:
                title = " ".join(largest_titles) if largest_titles else "Unknown Title"  # Combine remaining valid titles
            else:
                title = "Unknown Title"
        else:
            title = "Unknown Title"

        return title

    except Exception as e:
        error_message = f"Error extracting title: {str(e)}"
        # Print the traceback for more detailed error info
        print("Exception details:")
        print(traceback.format_exc())
        return error_message

    except Exception as e:
        error_message = f"Error extracting title: {str(e)}"
        # Print the traceback for more detailed error info
        print("Exception details:")
        print(traceback.format_exc())
        return error_message
    


def extract_text_from_pdf(file_content, filename, heading):
    """Extract all text lines after a specified heading in a PDF."""
    try:
        # Open the PDF using PyMuPDF (fitz)
        document = fitz.open(stream=file_content, filetype="pdf")
        section_text = []
        count = 0
        size = 0  # Default font size is 0
        color = (0, 0, 0)  # Default color is black
        font = "unknown"  # Default font is unknown
        # height = 0  # Default height is 0
        # width = 0  # Default width is 0
        # block_num = -9999999999999999
        
        title = extract_title_from_pdf(document)

        # Normalize the heading for case-insensitive matching
        normalized_heading = re.escape(heading.strip().lower())

        # Iterate through the pages to extract the section
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            if count == 3:
                break

            # Extract text in 'dict' format
            text_dict = page.get_text("dict")
            if "blocks" not in text_dict:
                continue  # Skip pages without 'blocks'

            # Iterate over blocks
            for block in text_dict["blocks"]:
                # block_number = block.get("number", 0)
                # print(f"Block number: {block_number}")
                # if block_number == block_num+2:
                #     count = 3
                #     break
                
                if count == 3:
                    break
                
                if block.get("type", -1) == 0:  # Ensure it's a text block
                    for line in block.get("lines", []):  # Iterate over lines
                        if count == 3:
                            break
                        
                        for span in line.get("spans", []):
                            line_text = span.get("text", "").strip()

                            # If heading is found, start appending subsequent lines
                            if line_text and count == 1:
                                size = round(span.get("size", 0))
                                color = span.get("color", (0, 0, 0))
                                font = span.get("font", "unknown")
                                # height = span.get("height", 0)
                                # width = span.get("width", 0)
                                # print(color, font, size, height, width)
                                count = 2  # Reset the flag
                                
                            if (line_text == "") and count == 2:
                                count = 3
                                break

                            if line_text and count == 2:
                                # if color == span.get("color", (0, 0, 0)) and font == span.get("font", "unknown") and size == round(span.get("size", 0)):
                                # if size == round(span.get("size", 0)) and height == span.get("height", 0) and width == span.get("width", 0):
                                if size == round(span.get("size", 0)) and (not line_text.isupper() or color == span.get("color", (0, 0, 0))):
                                    section_text.append(line_text)
                                else:
                                    count = 3
                                    break
                            
                            if line_text and count == 1:
                                section_text.append(line_text)
                                    
                            # Check if the line matches the heading
                            if count == 0 and re.search(
                                rf"^{normalized_heading}[:]?.*", line_text.lower(), re.IGNORECASE
                            ):
                                count = 1 # Heading found, start capturing from next line
                                # block_num = block.get("number", 0)  # Store the block number
                                # print("found")
                                # print(block_num)

        document.close()

        return {
            "fileName": filename,
            "title": title,
            "heading": heading,
            "paragraph": ' '.join(section_text).strip() or "No paragraph found for the specified heading."
        }
    except Exception as e:
        return {
            "fileName": filename,
            "title": "Error",
            "heading": heading,
            "paragraph": f"Error processing file: {str(e)}",
        }



def research_files_searching():
    """Handle the file upload and process files in parallel."""
    try:
        heading = request.form["heading"]
        files = request.files.getlist("files")
        
        print(f"Received heading: {heading}")
        print(f"Received files: {[file.filename for file in files]}")

        # Prepare file contents for processing
        file_data = [
            {"content": file.read(), "filename": file.filename} for file in files
        ]

        # Use ProcessPoolExecutor for parallel processing
        results = []
        with ProcessPoolExecutor() as executor:
            futures = []
            
            for data in file_data:
                # Submit the file content and filename to the worker function
                futures.append(
                    executor.submit(
                        extract_text_from_pdf,
                        data["content"],
                        data["filename"],
                        heading
                    )
                )

            for future in as_completed(futures):
                matches = future.result()
                if matches:
                    results.append(matches)

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


