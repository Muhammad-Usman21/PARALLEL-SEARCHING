from flask import Flask, request, jsonify
import pdfplumber  # You can use pdfplumber for easier PDF text extraction

def research_files_searching():
    research_paper_headings = [
        "Title",  # The title of the paper
        "Abstract",  # A brief summary of the research paper
        "Keywords",  # Keywords that summarize the content
        "Introduction",  # The introduction to the topic and research problem
        "Literature Review",  # Review of related work and existing research
        "Methodology",  # Methods used in the research
        "Data Collection",  # Description of how data was gathered
        "Data Analysis",  # Analysis techniques used on the collected data
        "Results",  # Results and findings from the research
        "Discussion",  # Interpretation of the results
        "Conclusion",  # The conclusion summarizing the findings and implications
        "References",  # List of cited sources
        "Acknowledgements",  # Recognition of people or organizations who contributed
        "Appendices",  # Supplementary material and details (e.g., charts, raw data)
        "Figures",  # All figures/tables/graphs used in the paper
        "Limitations",  # Any limitations of the study or research
        "Future Work",  # Suggested areas for future research
        "Supplementary Information",  # Additional data or resources that support the paper
        "Author Information",  # Information about the authors of the paper
        "Citations",  # Citations of the paper in other works
    ]

    try:
        heading = request.form["heading"]
        files = request.files.getlist("files")

        search_results = []

        # Process each uploaded file
        for file in files:
            pdf = pdfplumber.open(file)
            title = ""
            paragraph = ""

            # Extract the text from the entire document
            text_content = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                text_content += page_text

            # Title extraction: first non-empty line in the first page
            first_lines = text_content.split("\n")[:5]
            title = next((line for line in first_lines if len(line.strip()) > 5), "Unknown Title")

            # Search for the specified heading and extract the paragraph
            start_index = text_content.lower().find(heading.lower())
            if start_index != -1:
                start_index += len(heading)  # Move past the heading itself
                # Find the next heading to determine where the paragraph ends
                next_heading_index = None
                for next_heading in research_paper_headings:
                    if next_heading.lower() != heading.lower():
                        next_heading_index = text_content.lower().find(next_heading.lower(), start_index)
                        if next_heading_index != -1:
                            break
                
                if next_heading_index != -1:
                    end_index = next_heading_index
                else:
                    end_index = len(text_content)  # If no next heading is found, extract till the end of the document
                
                paragraph = text_content[start_index:end_index].strip()

            search_results.append({
                "fileName": file.filename,
                "title": title,
                "heading": heading,
                "paragraph": paragraph or "No paragraph found for the specified heading.",
            })

        return jsonify(search_results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
