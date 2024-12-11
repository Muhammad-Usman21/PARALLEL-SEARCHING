from flask import Flask, request, jsonify, send_file
from fpdf import FPDF
import os
import re

def sanitize_text(text):
    """Remove all non-ASCII characters from the given text."""
    return re.sub(r'[^\x00-\x7F]+', '', text)  # Matches and removes non-ASCII characters

def generate_pdf():
    data_object = request.json  # Get data sent from the frontend
    if not data_object or not data_object.get("searchResults"):
        return jsonify({"error": "No search results available to download."}), 400

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)

    # Add the main heading and pattern
    pdf.set_font("Times", style="B", size=20)
    pdf.multi_cell(0, 10, sanitize_text(f"Search Results for {data_object['pattern'].upper()}"), align="C")
    pdf.ln(3)  # Add some space after the heading

    # Add subheading with files
    pdf.set_font("Times", size=14)
    pdf.multi_cell(0, 8, sanitize_text(f"From Files: {', '.join(data_object['files'])}"), align="C")
    pdf.ln(3)  # Add some space after the subheading

    # Add search results
    for result in data_object["searchResults"]:
        pdf.ln(5)
        pdf.set_draw_color(150)  # Divider color
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Divider line
        pdf.ln(5)

        pdf.set_font("Times", size=14)
        pdf.multi_cell(0, 10, sanitize_text(f"{result['fileName']}"))
        pdf.ln(3)  # Adds some space after the file name

        # Title
        pdf.set_font("Times", style="B", size=20)
        pdf.multi_cell(0, 10, sanitize_text(result.get("title", "Untitled")), align="C")
        pdf.ln(3)  # Adds some space after the title

        # Heading
        heading = result.get("heading", "No Heading Found")
        pdf.set_font("Times", style="B", size=15)
        pdf.multi_cell(0, 10, sanitize_text(heading.capitalize()))
        pdf.ln(3)  # Adds some space after the heading

        # Paragraph
        paragraph = result.get("paragraph", "No Paragraph Found")
        pdf.set_font("Times", size=12)
        pdf.multi_cell(0, 6, sanitize_text(paragraph), align="J")

    # Save the PDF
    # output_file = f"{data_object['pattern']}-{len(data_object['files'])}files.pdf"
    output_file = f"output-file.pdf"
    pdf.output(output_file)

    # Send the PDF back to the client
    return send_file(output_file, as_attachment=True)
