from flask import Flask, request, jsonify, send_file
from fpdf import FPDF
import os

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
    pdf.cell(0, 10, f"Search Results for {data_object['pattern'].upper()}", align="C", ln=1)
    pdf.ln(3)

    # Add subheading with files
    pdf.set_font("Times", size=16)
    pdf.cell(0, 10, f"From Files: {', '.join(data_object['files'])}", align="C", ln=1)

    # Add search results
    for result in data_object["searchResults"]:
        pdf.ln(5)
        pdf.set_draw_color(150)  # Divider color
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())  # Divider line
        pdf.ln(5)

        # File name
        pdf.set_font("Times", size=14)
        pdf.cell(0, 10, f"{result['fileName']}", ln=1)

        # Title
        pdf.set_font("Times", style="B", size=20)
        pdf.cell(0, 10, result.get("title", "Untitled"), align="C", ln=1)

        # Heading
        heading = result.get("heading", "No Heading Found")
        pdf.set_font("Times", style="B", size=14)
        pdf.cell(0, 10, heading.capitalize(), ln=1)

        # Paragraph
        paragraph = result.get("paragraph", "No Paragraph Found")
        pdf.set_font("Times", size=12)
        pdf.multi_cell(0, 6, paragraph, align="J")

    # Save the PDF
    # output_file = f"{data_object['pattern']}-{len(data_object['files'])}files.pdf"
    output_file = f"output-file.pdf"
    pdf.output(output_file)

    # Send the PDF back to the client
    return send_file(output_file, as_attachment=True)
