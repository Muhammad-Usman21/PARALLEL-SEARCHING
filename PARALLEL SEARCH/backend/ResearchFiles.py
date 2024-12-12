from flask import Flask, request, jsonify
from concurrent.futures import ProcessPoolExecutor, as_completed
import fitz  
import re
import traceback
import os



def extract_title_from_pdf(document):
    """Title extraction based on font size and positioning in the whole document."""
    try:
        title = "Unknown Title"
        
        text_instances = []
        
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text_dict = page.get_text("dict")
            
            # print(f"Page {page_num} text data: {text_dict}")
            
            if "blocks" not in text_dict:
                raise ValueError(f"Missing 'blocks' in page {page_num} text data")
                
            text_instances += text_dict["blocks"]
        

        possible_titles = []
        
        for block in text_instances:
            if block.get("type", -1) == 0:  
                for line in block.get("lines", []): 
                    for span in line.get("spans", []): 
                        block_text = span.get("text", "").strip()
                        block_font_size = span.get("size", 4)

                        if block_text and len(block_text) > 5: 
                            if re.search(r"\d", block_text):
                                continue 

                            # print(f"Text: {block_text}, Font Size: {block_font_size}")
                            possible_titles.append((block_text, block_font_size))
                            
        if possible_titles:
            possible_titles.sort(key=lambda x: x[1], reverse=True)
            
            largest_font_size = possible_titles[0][1]

            largest_titles = [
                title[0]
                for title in possible_titles
                if title[1] == largest_font_size
            ]

            if largest_titles:
                title = " ".join(largest_titles) if largest_titles else "Unknown Title"  
            else:
                title = "Unknown Title"
        else:
            title = "Unknown Title"

        return title

    except Exception as e:
        error_message = f"Error extracting title: {str(e)}"
        print("Exception details:")
        print(traceback.format_exc())
        return error_message

    except Exception as e:
        error_message = f"Error extracting title: {str(e)}"
        print("Exception details:")
        print(traceback.format_exc())
        return error_message
    


def extract_text_from_pdf(file_content, filename, heading):
    """Extract all text lines after a specified heading in a PDF."""
    try:
        print(f"Process {os.getpid()} starting to process file '{filename}'")

        document = fitz.open(stream=file_content, filetype="pdf")
        section_text = []
        count = 0
        size = 0  
        color = (0, 0, 0)  
        font = "unknown" 
        # height = 0  
        # width = 0 
        # block_num = -9999999999999999
        
        title = extract_title_from_pdf(document)

        normalized_heading = re.escape(heading.strip().lower())

        for page_num in range(len(document)):
            page = document.load_page(page_num)
            if count == 3:
                break

            text_dict = page.get_text("dict")
            if "blocks" not in text_dict:
                continue  

            for block in text_dict["blocks"]:
                if count == 3:
                    break
                
                if block.get("type", -1) == 0: 
                    for line in block.get("lines", []): 
                        if count == 3:
                            break
                        
                        for span in line.get("spans", []):
                            line_text = span.get("text", "").strip()

                            if line_text and count == 1:
                                size = round(span.get("size", 0))
                                color = span.get("color", (0, 0, 0))
                                font = span.get("font", "unknown")
                                # height = span.get("height", 0)
                                # width = span.get("width", 0)
                                # print(color, font, size, height, width)
                                count = 2
                                
                            if line_text and count == 2:
                                # if color == span.get("color", (0, 0, 0)) and font == span.get("font", "unknown") and size == round(span.get("size", 0)):
                                # if size == round(span.get("size", 0)) and height == span.get("height", 0) and width == span.get("width", 0):
                                if size == round(span.get("size", 0)) and (not line_text.isupper() or color == span.get("color", (0, 0, 0))):
                                    section_text.append(line_text)
                                else:
                                    count = 3
                                    break
                            
                            if (line_text == "") and count == 2:
                                count = 3
                                break
                        
                                    
                            if count == 0 and re.search(
                                rf"^{normalized_heading}[:]?.*", line_text.lower(), re.IGNORECASE
                            ):
                                count = 1

        document.close()
        
        print(f"Process {os.getpid()} ending to process file '{filename}'")

        return {
            "fileName": filename,
            "title": title,
            "heading": heading,
            "paragraph": ' '.join(section_text).strip() or "No paragraph found for the specified heading.",
            "processId": os.getpid(),
        }
    except Exception as e:
        return {
            "fileName": filename,
            "title": "Error",
            "heading": heading,
            "paragraph": f"Error processing file: {str(e)}",
            "processId": os.getpid(),
        }



def research_files_searching():
    try:
        heading = request.form["heading"]
        files = request.files.getlist("files")
        
        # print(f"Received heading: {heading}")
        # print(f"Received files: {[file.filename for file in files]}")

        file_data = [
            {"content": file.read(), "filename": file.filename} for file in files
        ]

        results = []
        with ProcessPoolExecutor() as executor:
            futures = []
            
            for data in file_data:
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
                    
                    
                    
        # process_files = {}

        # for entry in results:
        #     process_id = entry["processId"]
        #     file_name = entry["fileName"]
        #     if process_id not in process_files:
        #         process_files[process_id] = []
        #     process_files[process_id].append(file_name)

        # for process_id, files in process_files.items():
        #     print(f"Process ID {process_id} processed {len(files)} file(s):")
        #     for file in files:
        #         print(f"- {file}")


        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


